---
name: github-self-hosted-runner
description:
  Install, register, namespace, verify, or remove one or more GitHub Actions
  self-hosted runners on a Linux or macOS host. Use when a user provides a
  GitHub repository or organization URL and wants a persistent runner managed by
  systemd on Linux or launchd on macOS, including adding another
  repository-specific runner to a machine that already has runners.
---

# GitHub self-hosted runner

Create one isolated runner instance per repository or organization registration.
Detect the operating system first and use the matching service manager: systemd
on Linux or launchd on macOS. Determine the account that should own and run the
runner instead of assuming a fixed username or home directory.

On Linux, resolve the account and paths with:

```bash
RUNNER_USER="${RUNNER_USER:-${SUDO_USER:-$USER}}"
RUNNER_GROUP="$(id -gn "$RUNNER_USER")"
RUNNER_HOME="$(getent passwd "$RUNNER_USER" | cut -d: -f6)"
RUNNER_ROOT="$RUNNER_HOME/actions-runners"
```

On macOS, resolve the account without relying on `getent`:

```bash
RUNNER_USER="${RUNNER_USER:-${SUDO_USER:-$USER}}"
RUNNER_GROUP="$(id -gn "$RUNNER_USER")"
RUNNER_HOME="$(dscl . -read "/Users/$RUNNER_USER" NFSHomeDirectory | awk '{print $2}')"
RUNNER_ROOT="$RUNNER_HOME/actions-runners"
```

Validate that the values are non-empty and `RUNNER_HOME` exists. When commands
run through `sudo`, do not accidentally use root's `$USER` or `$HOME` as the
runner account.

Namespace every instance by target slug:

- Directory: `$RUNNER_ROOT/<slug>`
- Runner name: `<hostname>-<slug>`
- Custom label: `<slug>`
- Linux service: `github-actions-runner@<slug>.service`
- macOS launchd label: `com.github.actions.runner.<slug>`

For example, `https://github.com/owner/blog` uses directory `$RUNNER_ROOT/blog`,
runner name `<hostname>-blog`, and label `blog`.

## Required inputs

Obtain:

1. A repository URL such as `https://github.com/owner/repository`, or an
   organization URL such as `https://github.com/organization`.
2. A GitHub credential authorized to manage self-hosted runners:
   - classic PAT with `repo` scope for a repository, or
   - an appropriately scoped fine-grained token.

GitHub does not support account-wide runners for a personal user URL. If a
one-segment GitHub URL belongs to a personal account rather than an
organization, ask for a repository URL.

Treat credentials as secrets:

- Never print a token.
- Never include it in a service unit, repository, skill file, or persistent
  environment file.
- Put it in a mode-`0600` temporary file only for the registration operation,
  then securely delete it.
- Recommend rotating any token pasted into chat after setup.

## Preflight

1. Detect the hostname and architecture.
2. Convert architecture names for GitHub assets:
   - `x86_64` → `x64`
   - `aarch64` or `arm64` → `arm64`
3. Derive a lowercase filesystem-safe slug from the repository name or
   organization name. Allow only letters, digits, `_`, and `-`.
4. Check whether the destination directory, runner registration, or service
   already exists.
5. Check for active jobs before stopping, replacing, or removing an existing
   runner. Do not interrupt a job without user confirmation.
6. Ensure `curl`, `tar`, `python3`, and the platform service manager (`systemd`
   on Linux, `launchd` on macOS) are available.

If the instance already exists and is healthy, report that instead of creating a
duplicate. If reconfiguration is requested, unregister the old instance before
replacing it.

## Install the runner

Fetch release metadata from GitHub's official API:

```bash
curl -fsSL https://api.github.com/repos/actions/runner/releases/latest
```

Select the asset matching both operating system and architecture, named like
`actions-runner-linux-<arch>-<version>.tar.gz` on Linux or
`actions-runner-osx-<arch>-<version>.tar.gz` on macOS. Read its
`browser_download_url` and `digest`. Download to a temporary archive, verify the
SHA-256 digest, and only then extract it into `$RUNNER_ROOT/<slug>`.

Set ownership recursively to `$RUNNER_USER:$RUNNER_GROUP` (on macOS, use the
resolved group, commonly `staff`). Delete the temporary archive even when a
command fails.

Always use a fresh runner distribution for a new instance. Do not copy
`.runner`, `.credentials`, `_diag`, or `_work` from another instance.

## Register

Run `config.sh` as `$RUNNER_USER` from inside the instance directory. The
working directory matters because runner scripts use relative paths.

Use:

```bash
./config.sh \
  --url '<github-url>' \
  --pat "$GITHUB_TOKEN" \
  --unattended \
  --name '<hostname>-<slug>' \
  --labels '<slug>' \
  --replace
```

Pass the PAT from the protected temporary file and securely remove that file
immediately afterward. Do not persist the PAT; GitHub exchanges it for runner
credentials during registration.

Do not use `--replace` to overwrite an unrelated live runner. Confirm that an
existing runner with the same name belongs to this VM and target.

## Configure the service manager

### Linux: systemd

Render a reusable template unit at
`/etc/systemd/system/github-actions-runner@.service` using the resolved runner
account values. Expand shell variables while writing the unit; systemd does not
expand them in these fields:

```bash
sudo tee /etc/systemd/system/github-actions-runner@.service >/dev/null <<EOF
[Unit]
Description=GitHub Actions self-hosted runner (%i)
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=${RUNNER_USER}
Group=${RUNNER_GROUP}
WorkingDirectory=${RUNNER_ROOT}/%i
ExecStart=${RUNNER_ROOT}/%i/run.sh
Restart=always
RestartSec=5
KillSignal=SIGINT
TimeoutStopSec=90

[Install]
WantedBy=multi-user.target
EOF
```

Then run:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now github-actions-runner@<slug>.service
```

Before replacing an existing template, inspect it and confirm its user and root
directory match the resolved values. Do not disrupt instances owned by another
account.

### macOS: launchd

Create a per-instance LaunchDaemon plist at
`/Library/LaunchDaemons/com.github.actions.runner.<slug>.plist`. Set `UserName`,
`GroupName`, `WorkingDirectory`, and `ProgramArguments` to the resolved account,
group, and instance path. Use `<RUNNER_ROOT>/<slug>/run.sh` as the program, set
`RunAtLoad` and `KeepAlive` to true, and do not put credentials in the plist.
Make the plist root-owned with mode `0644`, then load it with
`sudo launchctl bootstrap system <plist-path>`. Use
`sudo launchctl kickstart -k system/<label>` to start or restart the instance
after confirming it has no active job. If the service is already bootstrapped,
inspect it before replacing it; do not unload unrelated runners.

Do not configure a Linux runner with systemd on macOS or a macOS runner with
launchd on Linux.

## Verify

Verify the matching service manager. On Linux:

```bash
systemctl is-enabled github-actions-runner@<slug>.service
systemctl is-active github-actions-runner@<slug>.service
journalctl -u github-actions-runner@<slug>.service --no-pager -n 20
```

On macOS:

```bash
sudo launchctl print system/com.github.actions.runner.<slug>
tail -n 20 '<RUNNER_ROOT>/<slug>/_diag/Runner_*.log'
```

The runner log must show `Connected to GitHub` and `Listening for Jobs`.

Read `.runner` using UTF-8 with BOM support and confirm:

- `agentName` is `<hostname>-<slug>`
- `gitHubUrl` is the requested target
- `workFolder` is `_work`

Tell the user they can target the instance with:

```yaml
runs-on: [self-hosted, <slug>]
```

Report the runner name, directory, label, service, version, and active/listening
status. Do not repeat the token.

## Multiple runners on one VM

Each runner needs its own directory, local credentials, listener process, label,
and platform service instance. Multiple instances can run concurrently but share
the machine's CPU, memory, disk, network, and—when run as the same user—
filesystem trust boundary.

Use separate operating system users or separate machines for repositories that
should not trust each other's workflow code or files.

## Removal or renaming

To remove or rename an instance:

1. Confirm it is not running a job.
2. Disable and stop the platform service:
   `systemctl disable --now github-actions-runner@<slug>.service` on Linux, or
   `launchctl bootout system/<label>` on macOS.
3. Obtain a short-lived removal token through GitHub's repository or
   organization runner API using the PAT.
4. Run `./config.sh remove --token '<removal-token>'` from the runner directory
   as `$RUNNER_USER`.
5. For a rename, register again with the new runner name and restart the
   service.
6. For permanent removal, delete only that explicit instance directory after
   registration removal succeeds and the user confirms deletion.

Never delete the shared Linux systemd template while other instances use it. On
macOS, remove only the specific instance plist after unloading that instance.

## Full uninstall

Use this when removing every runner managed by this skill from the machine.
First inventory the registrations, instance directories, and services or plists;
do not assume every runner under a shared directory belongs to this setup.

1. Confirm that no runner is executing a job. Do not stop a busy runner without
   user confirmation.
2. Stop and disable each service. On Linux, run
   `sudo systemctl disable --now github-actions-runner@<slug>.service` for every
   instance, then confirm those units are inactive. On macOS, run
   `sudo launchctl bootout system/com.github.actions.runner.<slug>` for every
   loaded instance, then confirm those labels are no longer present.
3. For each instance, obtain a short-lived removal token from its GitHub
   repository or organization, then run
   `./config.sh remove --token '<removal-token>'` from that instance directory
   as `$RUNNER_USER`. Remove the token from memory and securely delete any
   temporary credential file.
4. Remove only the matching service configuration. On Linux, remove
   `/etc/systemd/system/github-actions-runner@.service` only after confirming
   that no other runner instances use it, then run
   `sudo systemctl daemon-reload`. On macOS, remove each matching plist from
   `/Library/LaunchDaemons/` after it has been unloaded.
5. Delete the explicit runner instance directories only after GitHub removal
   succeeds and the user confirms deleting the runner data. This removes
   binaries, credentials, diagnostics, and workspaces. Preserve unrelated files
   in `$RUNNER_ROOT`; remove that parent directory only if it is empty and the
   user confirms it should be removed.
6. Verify that the runner registrations are gone from GitHub, the services are
   absent or inactive, and no targeted instance directories or plists remain.

This procedure does not delete `$RUNNER_USER` or its home directory. Remove an
OS account only if it was created specifically for these runners, it owns no
other data or services, and the user explicitly requests account deletion. Never
remove system-wide dependencies such as Homebrew, Xcode, or command-line tools
as part of runner cleanup.

## Failure handling

- If registration fails, do not enable a restart-looping service.
- Preserve downloaded binaries when useful for retry, but remove all temporary
  credential files.
- A `404` from an organization registration endpoint often means the supplied
  one-segment URL is a personal account, the token lacks access, or the target
  is incorrect. Verify the target type before retrying.
- If extraction or checksum verification fails, remove the incomplete
  destination or clearly mark it incomplete; never start it.
- If the service starts but does not listen, inspect its journal on Linux or
  runner diagnostic logs on macOS; verify directory ownership, registration
  files, network access, and the service's working directory.
