# Notes: claim -> location (all paths relative to research/src at e246a25)

## Layout / reader (tensor.rs)

- MAX_HEADER_SIZE = 100_000_000; N_LEN = size_of::<u64>() = 8 -> tensor.rs:10-11
- read_metadata: get(..8) else HeaderTooSmall :392-394; u64::from_le_bytes :398;
  try_into usize else HeaderTooLarge :399-400; n > MAX -> HeaderTooLarge
  :402-404; checked_add else InvalidHeaderLength :406-408; buffer.get(8..stop)
  else InvalidHeaderLength :412-414; from_utf8 else InvalidHeader :415;
  serde_json::from_str else InvalidHeaderDeserialization :416-417; try_into
  (sort + Metadata::new -> validate) :418; validate again :419; buffer_end +
  N_LEN + n != buffer_len -> MetadataIncompleteBuffer :420-422
- HashMetadata: `__metadata__` Option<HashMap<String,String>>, flatten tensors
  HashMap<String,TensorInfo> :539-546
- TryFrom sorts by data_offsets :557; comment "Previous versions might have a
  different ordering" :553-556
- validate: s != start || e < s -> InvalidOffset(name) :631-638; checked_mul
  fold -> ValidationOverflow :642-650; nbits % 8 -> MisalignedSlice :652-654;
  e - s != size -> TensorInvalidInfo :659-661; returns start :663
- TensorInfo fields dtype, shape Vec<usize>, data_offsets (usize, usize);
  "Endianness is assumed to be little endian / Ordering is assumed to be 'C'"
  :795-806
- Dtype enum, "They MUST be in increasing alignment order" :808-863; bitsize
  :867-892
- deserialize: data = &buffer[N_LEN + n..] :446-450

## Writer (tensor.rs)

- prepare: sort_by right.dtype().cmp(left.dtype()).then(lname.cmp(rname))
  :229-232; offsets accumulate :236-248; serde_json::to_string :251;
  next_multiple_of(N_LEN), resize with b' ' :253-255
- serialize: n > MAX -> HeaderTooLarge :285-287; n.to_le_bytes :291
- buffered_write_to_file: NamedTempFile::new_in(parent) :313; set_len :315;
  F_NOCACHE macOS :319-324; BufWriter 1 MiB :327; persist (rename) :339
- Metadata::serialize writes **metadata** first then tensors in index order
  :574-597

## Python binding (bindings/python/src/lib.rs)

- parse_dtype_str names :155-186; TensorSpec F4 doubles last dim :74-84
- deserialize returns PyByteArray::new copy per tensor :281-302
- Open::new: File::open, FileNotFoundError :769-774; device check :777-784;
  map_copy_read_only :788; read_metadata :790-792; offset = n + 8 :794; Pread
  early return :814-824; torch UntypedStorage.from_file(shared=False, nbytes)
  :864-913; default Storage::Mmap :914
- keys() sorted :943-947; offset_keys :954-956
- get_tensor: Mmap -> PyByteArray::new(py, data) (copy) + create_tensor
  :1163-1177; Torch -> storage[start:stop], torch.asarray, view, reshape
  :1267-1349; pread -> PyByteArray::new_with + read_exact_at :1354-1384
- get_tensors loops offset_keys :1540-1547
- create_tensor: numpy frombuffer + reshape; zeros when count == 0 :2675-2743;
  byteswap on big-endian hosts :2732-2740
- get_pydtype: BF16 via numpy dtype("bfloat16"); F6 -> "Dtype not understood"
  :2809-2859
- parse_indexers: step must be positive :359-366; lists not implemented
  :312-323; one ellipsis :328-336
- slice: Mmap -> slice_bytes_to_tensor :2113-2118; Pread reads the whole tensor
  then slices :2119-2131
- backend names "mmap", "pread" :420-433; safe_open signature :1721

## Python (py_src/safetensors)

- numpy.\_flatten passes tensor.ctypes.data and tensor.nbytes, byteswaps
  non-little-endian, no contiguity check -> numpy.py:10-25
- numpy.load uses deserialize + np.frombuffer; \_TYPES has 13 entries ->
  numpy.py:98-181
- numpy.load_file = safe_open(framework="np", backend=backend).get_tensors() ->
  numpy.py:125-151
- torch.\_flatten_as_ptr raises on non-contiguous :575-581;
  \_evaluate_tensors_for_save rejects sparse and shared :527-563

## Prose spec (README.md)

- Format list :76-84; "MUST begin with a `{`" :78; "MAY be trailing padded with
  whitespace (0x20)" :79; metadata strings only :83
- Notes: duplicate keys :87; serde_json subset :88-91; NaN/Inf unchecked :92-93;
  empty tensors :94-97; 0-rank :98; no holes / polyglot :99-100; little-endian
  :101; C order :103
- Benefits: 100MB header limit, no overlap :170-175
- comparison table :118-129 (the author's "very personal and probably biased
  view" :116)

## Schema (docs/safetensors.schema.json)

- size_t maximum 281474976710655 (48 bits); dtype pattern
  "([UIF])(8|16|32|64|128|256)"; Tensor additionalProperties false; Metadata
  additionalProperties string
