# `std.win32_core`

Minimal pointer-correct Win32 substrate used by cross-platform std modules.
Keep C ABI pointers raw here; safe String/str wrappers belong in std.fs/os.

## Contents

- [Functions](#functions)

## Functions

### `create_file`

```quazi
pub fn create_file(path: *u8, access: u32, share: u32, security: *u8,
    disposition: u32, flags: u32, template: usize) usize
```

_Undocumented._

### `read_file`

```quazi
pub fn read_file(file: usize, buf: *u8, count: u32,
    read: *u32, overlapped: *u8) i32
```

_Undocumented._

### `write_file`

```quazi
pub fn write_file(file: usize, buf: *u8, count: u32,
    written: *u32, overlapped: *u8) i32
```

_Undocumented._

### `get_std_handle`

```quazi
pub fn get_std_handle(kind: u32) usize
```

_Undocumented._

### `get_console_mode`

```quazi
pub fn get_console_mode(console: usize, mode: *u32) i32
```

_Undocumented._

### `set_console_mode`

```quazi
pub fn set_console_mode(console: usize, mode: u32) i32
```

_Undocumented._

### `utf8_to_utf16`

```quazi
pub fn utf8_to_utf16(code_page: u32, flags: u32, input: *u8,
    input_len: i32, output: *u16, output_len: i32) i32
```

_Undocumented._

### `write_console_utf16`

```quazi
pub fn write_console_utf16(console: usize, text: *u16, count: u32,
    written: *u32, reserved: *u8) i32
```

_Undocumented._

### `close_handle`

```quazi
pub fn close_handle(handle: usize) i32
```

_Undocumented._

### `seek`

```quazi
pub fn seek(file: usize, distance: i64, position: *i64, method: u32) i32
```

_Undocumented._

### `set_socket_option`

```quazi
pub fn set_socket_option(socket: usize, level: i32, name: i32, value: *u8, length: i32) i32
```

_Undocumented._

### `get_current_directory`

```quazi
pub fn get_current_directory(length: u32, buffer: *u8) u32
```

ANSI-path working directory APIs, matching the other *A file APIs here.

### `set_current_directory`

```quazi
pub fn set_current_directory(path: *u8) i32
```

_Undocumented._

### `get_tick_count64`

```quazi
pub fn get_tick_count64() u64
```

_Undocumented._

### `get_system_time_as_file_time`

```quazi
pub fn get_system_time_as_file_time(file_time: *u8) void
```

FILETIME: 100-nanosecond intervals since 1601-01-01 UTC.

### `sync`

```quazi
pub fn sync(file: usize) i32
```

_Undocumented._

### `file_attributes`

```quazi
pub fn file_attributes(path: *u8) u32
```

_Undocumented._

### `file_attribute_data`

```quazi
pub fn file_attribute_data(path: *u8, level: i32, data: *u8) i32
```

level 0 (GetFileExInfoStandard) fills WIN32_FILE_ATTRIBUTE_DATA: attributes
at 0, creation/access/write FILETIMEs at 4/12/20, size high/low at 28/32.

### `delete_file`

```quazi
pub fn delete_file(path: *u8) i32
```

_Undocumented._

### `create_directory`

```quazi
pub fn create_directory(path: *u8, security: *u8) i32
```

_Undocumented._

### `remove_directory`

```quazi
pub fn remove_directory(path: *u8) i32
```

_Undocumented._

### `move_file`

```quazi
pub fn move_file(from: *u8, to: *u8) i32
```

_Undocumented._

### `environment`

```quazi
pub fn environment(name: *u8, buf: *u8, capacity: u32) u32
```

_Undocumented._

### `find_first`

```quazi
pub fn find_first(pattern: *u8, data: *u8) usize
```

_Undocumented._

### `find_next`

```quazi
pub fn find_next(handle: usize, data: *u8) i32
```

_Undocumented._

### `find_close`

```quazi
pub fn find_close(handle: usize) i32
```

_Undocumented._

### `last_error`

```quazi
pub fn last_error() u32
```

_Undocumented._

### `process_snapshot`

```quazi
pub fn process_snapshot(flags: u32, process: u32) usize
```

_Undocumented._

### `first_process`

```quazi
pub fn first_process(snapshot: usize, entry: *u8) i32
```

_Undocumented._

### `next_process`

```quazi
pub fn next_process(snapshot: usize, entry: *u8) i32
```

_Undocumented._

### `current_process_id`

```quazi
pub fn current_process_id() u32
```

_Undocumented._

### `winsock_startup`

```quazi
pub fn winsock_startup(version: u16, data: *u8) i32
```

Minimal pointer-correct Winsock2 substrate used by std.net.

### `winsock_cleanup`

```quazi
pub fn winsock_cleanup() i32
```

_Undocumented._

### `winsock_last_error`

```quazi
pub fn winsock_last_error() i32
```

_Undocumented._

### `socket`

```quazi
pub fn socket(af: i32, kind: i32, protocol: i32) usize
```

_Undocumented._

### `close_socket`

```quazi
pub fn close_socket(socket: usize) i32
```

_Undocumented._

### `listen_socket`

```quazi
pub fn listen_socket(socket: usize, backlog: i32) i32
```

_Undocumented._

### `accept_socket`

```quazi
pub fn accept_socket(socket: usize, address: *u8, address_length: *i32) usize
```

_Undocumented._

### `send_socket`

```quazi
pub fn send_socket(socket: usize, data: *u8, length: i32, flags: i32) i32
```

_Undocumented._

### `receive_socket`

```quazi
pub fn receive_socket(socket: usize, data: *u8, length: i32, flags: i32) i32
```

_Undocumented._

### `send_to_socket`

```quazi
pub fn send_to_socket(socket: usize, data: *u8, length: i32, flags: i32, address: *u8, address_length: i32) i32
```

_Undocumented._

### `receive_from_socket`

```quazi
pub fn receive_from_socket(socket: usize, data: *u8, length: i32, flags: i32, address: *u8, address_length: *i32) i32
```

_Undocumented._

### `shutdown_socket`

```quazi
pub fn shutdown_socket(socket: usize, how: i32) i32
```

_Undocumented._

### `load_library`

```quazi
pub fn load_library(path: *i8) usize
```

_Undocumented._

### `library_symbol`

```quazi
pub fn library_symbol(library: usize, name: *i8) usize
```

_Undocumented._

### `free_library`

```quazi
pub fn free_library(library: usize) i32
```

_Undocumented._

### `get_address_info`

```quazi
pub fn get_address_info(node: *i8, service: *i8, hints: *u8, result: **u8) i32
```

_Undocumented._

### `free_address_info`

```quazi
pub fn free_address_info(result: *u8) void
```

_Undocumented._

### `command_line_w`

```quazi
pub fn command_line_w() *u8
```

Process command line, split like the C runtime (UTF-16).

### `command_line_to_argv_w`

```quazi
pub fn command_line_to_argv_w(command_line: *u8, count: *i32) *u8
```

_Undocumented._

### `wide_to_multi_byte`

```quazi
pub fn wide_to_multi_byte(code_page: u32, flags: u32, wide: *u8, wide_length: i32,
    output: *u8, output_length: i32, default_char: *u8, used_default: *u8) i32
```

_Undocumented._

### `local_free`

```quazi
pub fn local_free(memory: *u8) *u8
```

_Undocumented._

### `full_path_name`

```quazi
pub fn full_path_name(path: *u8, length: u32, buffer: *u8, file_part: *u8) u32
```

Absolute form of a path (does not require it to exist or resolve links).
