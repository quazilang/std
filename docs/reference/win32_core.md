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

The Win32 function `CreateFileA` (see its Microsoft documentation).

### `read_file`

```quazi
pub fn read_file(file: usize, buf: *u8, count: u32,
    read: *u32, overlapped: *u8) i32
```

The Win32 function `ReadFile` (see its Microsoft documentation).

### `write_file`

```quazi
pub fn write_file(file: usize, buf: *u8, count: u32,
    written: *u32, overlapped: *u8) i32
```

The Win32 function `WriteFile` (see its Microsoft documentation).

### `get_std_handle`

```quazi
pub fn get_std_handle(kind: u32) usize
```

The Win32 function `GetStdHandle` (see its Microsoft documentation).

### `get_console_mode`

```quazi
pub fn get_console_mode(console: usize, mode: *u32) i32
```

The Win32 function `GetConsoleMode` (see its Microsoft documentation).

### `set_console_mode`

```quazi
pub fn set_console_mode(console: usize, mode: u32) i32
```

The Win32 function `SetConsoleMode` (see its Microsoft documentation).

### `utf8_to_utf16`

```quazi
pub fn utf8_to_utf16(code_page: u32, flags: u32, input: *u8,
    input_len: i32, output: *u16, output_len: i32) i32
```

The Win32 function `MultiByteToWideChar` (see its Microsoft documentation).

### `write_console_utf16`

```quazi
pub fn write_console_utf16(console: usize, text: *u16, count: u32,
    written: *u32, reserved: *u8) i32
```

The Win32 function `WriteConsoleW` (see its Microsoft documentation).

### `create_process_w`

```quazi
pub fn create_process_w(application: *u16, command_line: *u16,
    process_attributes: *u8, thread_attributes: *u8, inherit_handles: i32,
    creation_flags: u32, environment: *u8, current_directory: *u16,
    startup_info: *u8, process_information: *u8) i32
```

The Win32 function `CreateProcessW` (see its Microsoft documentation).

### `wait_for_single_object`

```quazi
pub fn wait_for_single_object(handle: usize, milliseconds: u32) u32
```

The Win32 function `WaitForSingleObject` (see its Microsoft documentation).

### `get_exit_code_process`

```quazi
pub fn get_exit_code_process(handle: usize, exit_code: *u32) i32
```

The Win32 function `GetExitCodeProcess` (see its Microsoft documentation).

### `terminate_process`

```quazi
pub fn terminate_process(handle: usize, exit_code: u32) i32
```

The Win32 function `TerminateProcess` (see its Microsoft documentation).

### `create_pipe`

```quazi
pub fn create_pipe(read_pipe: *usize, write_pipe: *usize, attributes: *u8, size: u32) i32
```

The Win32 function `CreatePipe` (see its Microsoft documentation).

### `set_handle_information`

```quazi
pub fn set_handle_information(handle: usize, mask: u32, flags: u32) i32
```

The Win32 function `SetHandleInformation` (see its Microsoft documentation).

### `peek_named_pipe`

```quazi
pub fn peek_named_pipe(pipe: usize, buffer: *u8, size: u32, read: *u32,
    available: *u32, left: *u32) i32
```

The Win32 function `PeekNamedPipe` (see its Microsoft documentation).

### `close_handle`

```quazi
pub fn close_handle(handle: usize) i32
```

The Win32 function `CloseHandle` (see its Microsoft documentation).

### `seek`

```quazi
pub fn seek(file: usize, distance: i64, position: *i64, method: u32) i32
```

The Win32 function `SetFilePointerEx` (see its Microsoft documentation).

### `set_socket_option`

```quazi
pub fn set_socket_option(socket: usize, level: i32, name: i32, value: *u8, length: i32) i32
```

The Win32 function `setsockopt` (see its Microsoft documentation).

### `get_current_directory`

```quazi
pub fn get_current_directory(length: u32, buffer: *u8) u32
```

ANSI-path working directory APIs, matching the other *A file APIs here.

### `set_current_directory`

```quazi
pub fn set_current_directory(path: *u8) i32
```

The Win32 function `SetCurrentDirectoryA` (see its Microsoft documentation).

### `get_tick_count64`

```quazi
pub fn get_tick_count64() u64
```

The Win32 function `GetTickCount64` (see its Microsoft documentation).

### `get_system_time_as_file_time`

```quazi
pub fn get_system_time_as_file_time(file_time: *u8) void
```

FILETIME: 100-nanosecond intervals since 1601-01-01 UTC.

### `sync`

```quazi
pub fn sync(file: usize) i32
```

The Win32 function `FlushFileBuffers` (see its Microsoft documentation).

### `file_attributes`

```quazi
pub fn file_attributes(path: *u8) u32
```

The Win32 function `GetFileAttributesA` (see its Microsoft documentation).

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

The Win32 function `DeleteFileA` (see its Microsoft documentation).

### `create_directory`

```quazi
pub fn create_directory(path: *u8, security: *u8) i32
```

The Win32 function `CreateDirectoryA` (see its Microsoft documentation).

### `remove_directory`

```quazi
pub fn remove_directory(path: *u8) i32
```

The Win32 function `RemoveDirectoryA` (see its Microsoft documentation).

### `move_file`

```quazi
pub fn move_file(from: *u8, to: *u8) i32
```

The Win32 function `MoveFileA` (see its Microsoft documentation).

### `environment`

```quazi
pub fn environment(name: *u8, buf: *u8, capacity: u32) u32
```

The Win32 function `GetEnvironmentVariableA` (see its Microsoft documentation).

### `environment_strings`

```quazi
pub fn environment_strings() *u8
```

The Win32 function `GetEnvironmentStringsA` (see its Microsoft documentation).

### `free_environment_strings`

```quazi
pub fn free_environment_strings(block: *u8) i32
```

The Win32 function `FreeEnvironmentStringsA` (see its Microsoft documentation).

### `set_environment`

```quazi
pub fn set_environment(name: *u8, value: *u8) i32
```

The Win32 function `SetEnvironmentVariableA` (see its Microsoft documentation).
A null `value` removes the variable.

### `find_first`

```quazi
pub fn find_first(pattern: *u8, data: *u8) usize
```

The Win32 function `FindFirstFileA` (see its Microsoft documentation).

### `find_next`

```quazi
pub fn find_next(handle: usize, data: *u8) i32
```

The Win32 function `FindNextFileA` (see its Microsoft documentation).

### `find_close`

```quazi
pub fn find_close(handle: usize) i32
```

The Win32 function `FindClose` (see its Microsoft documentation).

### `last_error`

```quazi
pub fn last_error() u32
```

The Win32 function `GetLastError` (see its Microsoft documentation).

### `set_last_error`

```quazi
pub fn set_last_error(code: u32) void
```

The Win32 function `SetLastError` (see its Microsoft documentation).

### `process_snapshot`

```quazi
pub fn process_snapshot(flags: u32, process: u32) usize
```

The Win32 function `CreateToolhelp32Snapshot` (see its Microsoft documentation).

### `first_process`

```quazi
pub fn first_process(snapshot: usize, entry: *u8) i32
```

The Win32 function `Process32First` (see its Microsoft documentation).

### `next_process`

```quazi
pub fn next_process(snapshot: usize, entry: *u8) i32
```

The Win32 function `Process32Next` (see its Microsoft documentation).

### `current_process_id`

```quazi
pub fn current_process_id() u32
```

The Win32 function `GetCurrentProcessId` (see its Microsoft documentation).

### `winsock_startup`

```quazi
pub fn winsock_startup(version: u16, data: *u8) i32
```

Minimal pointer-correct Winsock2 substrate used by std.net.

### `winsock_cleanup`

```quazi
pub fn winsock_cleanup() i32
```

The Win32 function `WSACleanup` (see its Microsoft documentation).

### `winsock_last_error`

```quazi
pub fn winsock_last_error() i32
```

The Win32 function `WSAGetLastError` (see its Microsoft documentation).

### `socket`

```quazi
pub fn socket(af: i32, kind: i32, protocol: i32) usize
```

The Win32 function `socket` (see its Microsoft documentation).

### `close_socket`

```quazi
pub fn close_socket(socket: usize) i32
```

The Win32 function `closesocket` (see its Microsoft documentation).

### `listen_socket`

```quazi
pub fn listen_socket(socket: usize, backlog: i32) i32
```

The Win32 function `listen` (see its Microsoft documentation).

### `accept_socket`

```quazi
pub fn accept_socket(socket: usize, address: *u8, address_length: *i32) usize
```

The Win32 function `accept` (see its Microsoft documentation).

### `send_socket`

```quazi
pub fn send_socket(socket: usize, data: *u8, length: i32, flags: i32) i32
```

The Win32 function `send` (see its Microsoft documentation).

### `receive_socket`

```quazi
pub fn receive_socket(socket: usize, data: *u8, length: i32, flags: i32) i32
```

The Win32 function `recv` (see its Microsoft documentation).

### `send_to_socket`

```quazi
pub fn send_to_socket(socket: usize, data: *u8, length: i32, flags: i32, address: *u8, address_length: i32) i32
```

The Win32 function `sendto` (see its Microsoft documentation).

### `receive_from_socket`

```quazi
pub fn receive_from_socket(socket: usize, data: *u8, length: i32, flags: i32, address: *u8, address_length: *i32) i32
```

The Win32 function `recvfrom` (see its Microsoft documentation).

### `shutdown_socket`

```quazi
pub fn shutdown_socket(socket: usize, how: i32) i32
```

The Win32 function `shutdown` (see its Microsoft documentation).

### `load_library`

```quazi
pub fn load_library(path: *i8) usize
```

The Win32 function `LoadLibraryA` (see its Microsoft documentation).

### `library_symbol`

```quazi
pub fn library_symbol(library: usize, name: *i8) usize
```

The Win32 function `GetProcAddress` (see its Microsoft documentation).

### `free_library`

```quazi
pub fn free_library(library: usize) i32
```

The Win32 function `FreeLibrary` (see its Microsoft documentation).

### `get_address_info`

```quazi
pub fn get_address_info(node: *i8, service: *i8, hints: *u8, result: **u8) i32
```

The Win32 function `getaddrinfo` (see its Microsoft documentation).

### `free_address_info`

```quazi
pub fn free_address_info(result: *u8) void
```

The Win32 function `freeaddrinfo` (see its Microsoft documentation).

### `command_line_w`

```quazi
pub fn command_line_w() *u8
```

Process command line, split like the C runtime (UTF-16).

### `command_line_to_argv_w`

```quazi
pub fn command_line_to_argv_w(command_line: *u8, count: *i32) *u8
```

The Win32 function `CommandLineToArgvW` (see its Microsoft documentation).

### `wide_to_multi_byte`

```quazi
pub fn wide_to_multi_byte(code_page: u32, flags: u32, wide: *u8, wide_length: i32,
    output: *u8, output_length: i32, default_char: *u8, used_default: *u8) i32
```

The Win32 function `WideCharToMultiByte` (see its Microsoft documentation).

### `local_free`

```quazi
pub fn local_free(memory: *u8) *u8
```

The Win32 function `LocalFree` (see its Microsoft documentation).

### `full_path_name`

```quazi
pub fn full_path_name(path: *u8, length: u32, buffer: *u8, file_part: *u8) u32
```

Absolute form of a path (does not require it to exist or resolve links).
