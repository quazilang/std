# `std.windows`

std.windows — Windows Win32 API bindings via @api
All functions use Win64 calling convention (rcx, rdx, r8, r9).
All functions are implicitly unsafe — callers must wrap in unsafe {}.

Required libs (add to quazi.toml [build].flags or linker invocation):
  kernel32.lib  — handles, process, memory, console, sync, registry
  user32.lib    — window/message API
  advapi32.lib  — registry, security, services
  ws2_32.lib    — WinSock2 networking

Type conventions:
  HANDLE / HMODULE / HWND / HKEY etc. → usize (opaque kernel handle, not dereffed)
  BOOL  → i32 (0 = FALSE, nonzero = TRUE)
  DWORD → u32
  WORD  → u16
  LPSTR / LPCSTR / char* → str (C string pointer, read-only)
  void* / struct* → *u8 (raw byte pointer to heap/stack data)
  LPDWORD / DWORD* → *u32 (out-parameter pointer to DWORD)
  SIZE_T → usize
  UINT / int → i32 or u32 depending on signedness

## Contents

- [Functions](#functions)

## Functions

### `get_std_handle`

```quazi
pub fn get_std_handle(n_std_handle: u32) usize
```

STD_INPUT_HANDLE  = 0xFFFFFFF6 (4294967286)
STD_OUTPUT_HANDLE = 0xFFFFFFF5 (4294967285)
STD_ERROR_HANDLE  = 0xFFFFFFF4 (4294967284)

### `close_handle`

```quazi
pub fn close_handle(object: usize) i32
```

The Win32 function `CloseHandle` (see its Microsoft documentation).

### `duplicate_handle`

```quazi
pub fn duplicate_handle(src_proc: usize, src: usize, dst_proc: usize, dst: *u8, access: u32, inherit: i32, options: u32) i32
```

dst: pointer to HANDLE output

### `write_file`

```quazi
pub fn write_file(file: usize, buf: str, n_to_write: u32, n_written: *u32, overlapped: *u8) i32
```

n_written: pointer to DWORD output (bytes written); overlapped: pointer to OVERLAPPED or null

### `read_file`

```quazi
pub fn read_file(file: usize, buf: str, n_to_read: u32, n_read: *u32, overlapped: *u8) i32
```

n_read: pointer to DWORD output (bytes read); overlapped: pointer to OVERLAPPED or null

### `write_console_a`

```quazi
pub fn write_console_a(console: usize, buf: str, n_chars: u32, n_written: *u32, reserved: *u8) i32
```

n_written: pointer to DWORD output; reserved: must be null

### `read_console_a`

```quazi
pub fn read_console_a(console: usize, buf: str, n_chars: u32, n_read: *u32, reserved: *u8) i32
```

n_read: pointer to DWORD output; reserved: must be null

### `flush_file_buffers`

```quazi
pub fn flush_file_buffers(file: usize) i32
```

The Win32 function `FlushFileBuffers` (see its Microsoft documentation).

### `get_console_mode`

```quazi
pub fn get_console_mode(console: usize, mode: *u32) i32
```

mode: pointer to DWORD output

### `set_console_mode`

```quazi
pub fn set_console_mode(console: usize, mode: u32) i32
```

The Win32 function `SetConsoleMode` (see its Microsoft documentation).

### `set_console_title_a`

```quazi
pub fn set_console_title_a(title: str) i32
```

The Win32 function `SetConsoleTitleA` (see its Microsoft documentation).

### `set_console_text_attribute`

```quazi
pub fn set_console_text_attribute(console: usize, attr: u16) i32
```

attr: combination of FOREGROUND_*/BACKGROUND_* constants

### `alloc_console`

```quazi
pub fn alloc_console() i32
```

The Win32 function `AllocConsole` (see its Microsoft documentation).

### `free_console`

```quazi
pub fn free_console() i32
```

The Win32 function `FreeConsole` (see its Microsoft documentation).

### `get_console_window`

```quazi
pub fn get_console_window() usize
```

The Win32 function `GetConsoleWindow` (see its Microsoft documentation).

### `create_file_a`

```quazi
pub fn create_file_a(path: str, access: u32, share: u32, security: *u8, disposition: u32, flags: u32, template: usize) usize
```

security: pointer to SECURITY_ATTRIBUTES or null; template: file handle or null
access: GENERIC_READ=0x80000000, GENERIC_WRITE=0x40000000
share: FILE_SHARE_READ=1, FILE_SHARE_WRITE=2
disposition: CREATE_NEW=1, CREATE_ALWAYS=2, OPEN_EXISTING=3, OPEN_ALWAYS=4, TRUNCATE_EXISTING=5
flags: FILE_ATTRIBUTE_NORMAL=128, FILE_FLAG_OVERLAPPED=0x40000000

### `get_file_size`

```quazi
pub fn get_file_size(file: usize, high: *u32) u32
```

high: pointer to DWORD for high 32 bits of size (or null)

### `get_file_size_ex`

```quazi
pub fn get_file_size_ex(file: usize, size: *i64) i32
```

size: pointer to LARGE_INTEGER (i64) output

### `set_file_pointer`

```quazi
pub fn set_file_pointer(file: usize, dist_low: i32, dist_high: *i32, method: u32) u32
```

method: FILE_BEGIN=0, FILE_CURRENT=1, FILE_END=2
dist_high: pointer to i32 high word (or null)

### `set_file_pointer_ex`

```quazi
pub fn set_file_pointer_ex(file: usize, dist: i64, new_ptr: *i64, method: u32) i32
```

new_ptr: pointer to LARGE_INTEGER output for new position (or null)

### `delete_file_a`

```quazi
pub fn delete_file_a(path: str) i32
```

The Win32 function `DeleteFileA` (see its Microsoft documentation).

### `move_file_a`

```quazi
pub fn move_file_a(existing: str, new_path: str) i32
```

The Win32 function `MoveFileA` (see its Microsoft documentation).

### `copy_file_a`

```quazi
pub fn copy_file_a(existing: str, new_path: str, fail_if_exists: i32) i32
```

The Win32 function `CopyFileA` (see its Microsoft documentation).

### `create_directory_a`

```quazi
pub fn create_directory_a(path: str, security: *u8) i32
```

security: pointer to SECURITY_ATTRIBUTES or null

### `remove_directory_a`

```quazi
pub fn remove_directory_a(path: str) i32
```

The Win32 function `RemoveDirectoryA` (see its Microsoft documentation).

### `get_current_directory_a`

```quazi
pub fn get_current_directory_a(buf_len: u32, buf: str) u32
```

The Win32 function `GetCurrentDirectoryA` (see its Microsoft documentation).

### `set_current_directory_a`

```quazi
pub fn set_current_directory_a(path: str) i32
```

The Win32 function `SetCurrentDirectoryA` (see its Microsoft documentation).

### `find_first_file_a`

```quazi
pub fn find_first_file_a(pattern: str, data: *u8) usize
```

data: pointer to WIN32_FIND_DATAA struct output; returns search handle

### `find_next_file_a`

```quazi
pub fn find_next_file_a(handle: usize, data: *u8) i32
```

The Win32 function `FindNextFileA` (see its Microsoft documentation).

### `find_close`

```quazi
pub fn find_close(handle: usize) i32
```

The Win32 function `FindClose` (see its Microsoft documentation).

### `get_temp_path_a`

```quazi
pub fn get_temp_path_a(buf_len: u32, buf: str) u32
```

The Win32 function `GetTempPathA` (see its Microsoft documentation).

### `get_temp_file_name_a`

```quazi
pub fn get_temp_file_name_a(path: str, prefix: str, unique: u32, name: str) u32
```

The Win32 function `GetTempFileNameA` (see its Microsoft documentation).

### `get_file_attributes_a`

```quazi
pub fn get_file_attributes_a(path: str) u32
```

The Win32 function `GetFileAttributesA` (see its Microsoft documentation).

### `set_file_attributes_a`

```quazi
pub fn set_file_attributes_a(path: str, attrs: u32) i32
```

The Win32 function `SetFileAttributesA` (see its Microsoft documentation).

### `get_current_process`

```quazi
pub fn get_current_process() usize
```

The Win32 function `GetCurrentProcess` (see its Microsoft documentation).

### `get_current_process_id`

```quazi
pub fn get_current_process_id() u32
```

The Win32 function `GetCurrentProcessId` (see its Microsoft documentation).

### `get_current_thread_id`

```quazi
pub fn get_current_thread_id() u32
```

The Win32 function `GetCurrentThreadId` (see its Microsoft documentation).

### `exit_process`

```quazi
pub fn exit_process(exit_code: u32) void
```

The Win32 function `ExitProcess` (see its Microsoft documentation).

### `create_process_a`

```quazi
pub fn create_process_a(app: str, cmd: str, proc_sec: *u8, thread_sec: *u8, inherit: i32, flags: u32, env: *u8, dir: str, startup: *u8, proc_info: *u8) i32
```

proc_sec/thread_sec: pointer to SECURITY_ATTRIBUTES or null
env: pointer to environment block or null (inherit parent)
startup: pointer to STARTUPINFOA; proc_info: pointer to PROCESS_INFORMATION output
creation_flags: CREATE_NEW_CONSOLE=0x10, CREATE_SUSPENDED=0x4, DETACHED_PROCESS=0x8

### `open_process`

```quazi
pub fn open_process(access: u32, inherit: i32, pid: u32) usize
```

access: PROCESS_ALL_ACCESS=0x1FFFFF, PROCESS_QUERY_INFORMATION=0x400

### `terminate_process`

```quazi
pub fn terminate_process(proc: usize, exit_code: u32) i32
```

The Win32 function `TerminateProcess` (see its Microsoft documentation).

### `get_exit_code_process`

```quazi
pub fn get_exit_code_process(proc: usize, exit_code: *u32) i32
```

exit_code: pointer to DWORD output

### `get_exit_code_thread`

```quazi
pub fn get_exit_code_thread(thread: usize, exit_code: *u32) i32
```

The Win32 function `GetExitCodeThread` (see its Microsoft documentation).

### `wait_for_single_object`

```quazi
pub fn wait_for_single_object(handle: usize, ms: u32) u32
```

milliseconds: INFINITE=0xFFFFFFFF

### `wait_for_multiple_objects`

```quazi
pub fn wait_for_multiple_objects(count: u32, handles: *u8, wait_all: i32, ms: u32) u32
```

handles: pointer to HANDLE[] array

### `create_thread`

```quazi
pub fn create_thread(security: *u8, stack_size: usize, start_routine: usize, param: *u8, flags: u32, thread_id: *u32) usize
```

security: pointer to SECURITY_ATTRIBUTES or null
start_routine: function pointer (LPTHREAD_START_ROUTINE) — pass as usize until fn ptr support
param: pointer to thread parameter (or null)
thread_id: pointer to DWORD output for thread ID (or null)
creation_flags: 0 = run immediately, CREATE_SUSPENDED=4

### `exit_thread`

```quazi
pub fn exit_thread(exit_code: u32) void
```

The Win32 function `ExitThread` (see its Microsoft documentation).

### `get_current_thread`

```quazi
pub fn get_current_thread() usize
```

The Win32 function `GetCurrentThread` (see its Microsoft documentation).

### `resume_thread`

```quazi
pub fn resume_thread(thread: usize) u32
```

The Win32 function `ResumeThread` (see its Microsoft documentation).

### `suspend_thread`

```quazi
pub fn suspend_thread(thread: usize) u32
```

The Win32 function `SuspendThread` (see its Microsoft documentation).

### `terminate_thread`

```quazi
pub fn terminate_thread(thread: usize, exit_code: u32) i32
```

The Win32 function `TerminateThread` (see its Microsoft documentation).

### `set_thread_priority`

```quazi
pub fn set_thread_priority(thread: usize, priority: i32) i32
```

priority: THREAD_PRIORITY_NORMAL=0, ABOVE_NORMAL=1, BELOW_NORMAL=-1, HIGHEST=2, LOWEST=-2

### `get_thread_priority`

```quazi
pub fn get_thread_priority(thread: usize) i32
```

The Win32 function `GetThreadPriority` (see its Microsoft documentation).

### `tls_alloc`

```quazi
pub fn tls_alloc() u32
```

The Win32 function `TlsAlloc` (see its Microsoft documentation).

### `tls_get_value`

```quazi
pub fn tls_get_value(index: u32) *u8
```

Returns pointer to thread-local value

### `tls_set_value`

```quazi
pub fn tls_set_value(index: u32, value: *u8) i32
```

value: pointer to thread-local data

### `tls_free`

```quazi
pub fn tls_free(index: u32) i32
```

The Win32 function `TlsFree` (see its Microsoft documentation).

### `sleep`

```quazi
pub fn sleep(ms: u32) void
```

The Win32 function `Sleep` (see its Microsoft documentation).

### `sleep_ex`

```quazi
pub fn sleep_ex(ms: u32, alertable: i32) u32
```

The Win32 function `SleepEx` (see its Microsoft documentation).

### `virtual_alloc`

```quazi
pub fn virtual_alloc(addr: *u8, size: usize, alloc_type: u32, protect: u32) *u8
```

addr: preferred base address or null for kernel choice; returns committed pointer or null
type: MEM_COMMIT=0x1000, MEM_RESERVE=0x2000, MEM_COMMIT|MEM_RESERVE=0x3000
protect: PAGE_READWRITE=4, PAGE_READONLY=2, PAGE_EXECUTE_READ=0x20, PAGE_EXECUTE_READWRITE=0x40

### `virtual_free`

```quazi
pub fn virtual_free(addr: *u8, size: usize, free_type: u32) i32
```

addr: pointer returned by VirtualAlloc; type: MEM_RELEASE=0x8000, MEM_DECOMMIT=0x4000

### `virtual_protect`

```quazi
pub fn virtual_protect(addr: *u8, size: usize, new_protect: u32, old_protect: *u32) i32
```

old_protect: pointer to DWORD output for previous protection flags

### `virtual_query`

```quazi
pub fn virtual_query(addr: *u8, buf: *u8, len: usize) usize
```

buf: pointer to MEMORY_BASIC_INFORMATION output

### `get_process_heap`

```quazi
pub fn get_process_heap() usize
```

Returns process heap handle

### `heap_alloc`

```quazi
pub fn heap_alloc(heap: usize, flags: u32, size: usize) *u8
```

flags: HEAP_ZERO_MEMORY=8; returns pointer to allocated block or null

### `heap_free`

```quazi
pub fn heap_free(heap: usize, flags: u32, mem: *u8) i32
```

mem: pointer previously returned by HeapAlloc/HeapReAlloc

### `heap_realloc`

```quazi
pub fn heap_realloc(heap: usize, flags: u32, mem: *u8, size: usize) *u8
```

mem: pointer to reallocate; returns new pointer or null on failure

### `heap_size`

```quazi
pub fn heap_size(heap: usize, flags: u32, mem: *u8) usize
```

Returns size of allocated block

### `heap_create`

```quazi
pub fn heap_create(options: u32, initial: usize, maximum: usize) usize
```

The Win32 function `HeapCreate` (see its Microsoft documentation).

### `heap_destroy`

```quazi
pub fn heap_destroy(heap: usize) i32
```

The Win32 function `HeapDestroy` (see its Microsoft documentation).

### `local_alloc`

```quazi
pub fn local_alloc(flags: u32, size: usize) *u8
```

flags: LMEM_FIXED=0, LMEM_ZEROINIT=0x40; returns pointer to allocated block

### `local_free`

```quazi
pub fn local_free(mem: *u8) *u8
```

mem: pointer returned by LocalAlloc; returns null on success, mem on failure

### `global_alloc`

```quazi
pub fn global_alloc(flags: u32, size: usize) *u8
```

The Win32 function `GlobalAlloc` (see its Microsoft documentation).

### `global_free`

```quazi
pub fn global_free(mem: *u8) *u8
```

The Win32 function `GlobalFree` (see its Microsoft documentation).

### `create_mutex_a`

```quazi
pub fn create_mutex_a(security: *u8, initial_owner: i32, name: str) usize
```

security: pointer to SECURITY_ATTRIBUTES or null; initial_owner: TRUE=1

### `open_mutex_a`

```quazi
pub fn open_mutex_a(access: u32, inherit: i32, name: str) usize
```

The Win32 function `OpenMutexA` (see its Microsoft documentation).

### `release_mutex`

```quazi
pub fn release_mutex(mutex: usize) i32
```

The Win32 function `ReleaseMutex` (see its Microsoft documentation).

### `create_event_a`

```quazi
pub fn create_event_a(security: *u8, manual_reset: i32, initial_state: i32, name: str) usize
```

security: pointer to SECURITY_ATTRIBUTES or null; manual_reset: TRUE=1 for manual

### `open_event_a`

```quazi
pub fn open_event_a(access: u32, inherit: i32, name: str) usize
```

The Win32 function `OpenEventA` (see its Microsoft documentation).

### `set_event`

```quazi
pub fn set_event(event: usize) i32
```

The Win32 function `SetEvent` (see its Microsoft documentation).

### `reset_event`

```quazi
pub fn reset_event(event: usize) i32
```

The Win32 function `ResetEvent` (see its Microsoft documentation).

### `pulse_event`

```quazi
pub fn pulse_event(event: usize) i32
```

The Win32 function `PulseEvent` (see its Microsoft documentation).

### `create_semaphore_a`

```quazi
pub fn create_semaphore_a(security: *u8, initial: i32, maximum: i32, name: str) usize
```

security: pointer to SECURITY_ATTRIBUTES or null

### `release_semaphore`

```quazi
pub fn release_semaphore(sem: usize, count: i32, prev: *i32) i32
```

prev: pointer to LONG output for previous count (or null)

### `initialize_critical_section`

```quazi
pub fn initialize_critical_section(cs: *u8) void
```

cs: pointer to CRITICAL_SECTION (40 bytes on x86-64)

### `enter_critical_section`

```quazi
pub fn enter_critical_section(cs: *u8) void
```

The Win32 function `EnterCriticalSection` (see its Microsoft documentation).

### `try_enter_critical_section`

```quazi
pub fn try_enter_critical_section(cs: *u8) i32
```

The Win32 function `TryEnterCriticalSection` (see its Microsoft documentation).

### `leave_critical_section`

```quazi
pub fn leave_critical_section(cs: *u8) void
```

The Win32 function `LeaveCriticalSection` (see its Microsoft documentation).

### `delete_critical_section`

```quazi
pub fn delete_critical_section(cs: *u8) void
```

The Win32 function `DeleteCriticalSection` (see its Microsoft documentation).

### `get_last_error`

```quazi
pub fn get_last_error() u32
```

The Win32 function `GetLastError` (see its Microsoft documentation).

### `set_last_error`

```quazi
pub fn set_last_error(err: u32) void
```

The Win32 function `SetLastError` (see its Microsoft documentation).

### `format_message_a`

```quazi
pub fn format_message_a(flags: u32, source: *u8, msg_id: u32, lang: u32, buf: str, size: u32, args: *u8) u32
```

source: module handle (when FORMAT_MESSAGE_FROM_HMODULE) or null
args: pointer to va_list or array of insert strings (or null with IGNORE_INSERTS)
flags: FORMAT_MESSAGE_FROM_SYSTEM=0x1000, FORMAT_MESSAGE_IGNORE_INSERTS=0x200

### `load_library_a`

```quazi
pub fn load_library_a(name: str) usize
```

The Win32 function `LoadLibraryA` (see its Microsoft documentation).

### `load_library_ex_a`

```quazi
pub fn load_library_ex_a(name: str, file: usize, flags: u32) usize
```

file: reserved, pass null

### `get_proc_address`

```quazi
pub fn get_proc_address(module: usize, name: str) usize
```

Returns function pointer as usize (cast to fn type before calling)

### `free_library`

```quazi
pub fn free_library(module: usize) i32
```

The Win32 function `FreeLibrary` (see its Microsoft documentation).

### `get_module_handle_a`

```quazi
pub fn get_module_handle_a(name: str) usize
```

The Win32 function `GetModuleHandleA` (see its Microsoft documentation).

### `get_module_file_name_a`

```quazi
pub fn get_module_file_name_a(module: usize, buf: str, size: u32) u32
```

The Win32 function `GetModuleFileNameA` (see its Microsoft documentation).

### `get_environment_variable_a`

```quazi
pub fn get_environment_variable_a(name: str, buf: str, size: u32) u32
```

The Win32 function `GetEnvironmentVariableA` (see its Microsoft documentation).

### `set_environment_variable_a`

```quazi
pub fn set_environment_variable_a(name: str, value: str) i32
```

The Win32 function `SetEnvironmentVariableA` (see its Microsoft documentation).

### `get_command_line_a`

```quazi
pub fn get_command_line_a() str
```

The Win32 function `GetCommandLineA` (see its Microsoft documentation).

### `get_environment_strings_a`

```quazi
pub fn get_environment_strings_a() *u8
```

Returns pointer to null-terminated block of null-terminated strings

### `free_environment_strings_a`

```quazi
pub fn free_environment_strings_a(env: *u8) i32
```

env: pointer returned by GetEnvironmentStringsA

### `get_system_time`

```quazi
pub fn get_system_time(st: *u8) void
```

st: pointer to SYSTEMTIME { u16 year, month, dow, day, hour, min, sec, ms }

### `get_local_time`

```quazi
pub fn get_local_time(st: *u8) void
```

The Win32 function `GetLocalTime` (see its Microsoft documentation).

### `set_system_time`

```quazi
pub fn set_system_time(st: *u8) i32
```

The Win32 function `SetSystemTime` (see its Microsoft documentation).

### `set_local_time`

```quazi
pub fn set_local_time(st: *u8) i32
```

The Win32 function `SetLocalTime` (see its Microsoft documentation).

### `get_system_time_as_file_time`

```quazi
pub fn get_system_time_as_file_time(ft: *u8) void
```

ft: pointer to FILETIME { u32 low, u32 high } — 100-nanosecond intervals since 1601-01-01

### `file_time_to_system_time`

```quazi
pub fn file_time_to_system_time(ft: *u8, st: *u8) i32
```

The Win32 function `FileTimeToSystemTime` (see its Microsoft documentation).

### `system_time_to_file_time`

```quazi
pub fn system_time_to_file_time(st: *u8, ft: *u8) i32
```

The Win32 function `SystemTimeToFileTime` (see its Microsoft documentation).

### `file_time_to_local_file_time`

```quazi
pub fn file_time_to_local_file_time(utc: *u8, local: *u8) i32
```

The Win32 function `FileTimeToLocalFileTime` (see its Microsoft documentation).

### `query_performance_counter`

```quazi
pub fn query_performance_counter(count: *i64) i32
```

count/freq: pointer to LARGE_INTEGER (i64) output

### `query_performance_frequency`

```quazi
pub fn query_performance_frequency(freq: *i64) i32
```

The Win32 function `QueryPerformanceFrequency` (see its Microsoft documentation).

### `get_tick_count64`

```quazi
pub fn get_tick_count64() u64
```

The Win32 function `GetTickCount64` (see its Microsoft documentation).

### `reg_open_key_ex_a`

```quazi
pub fn reg_open_key_ex_a(key: usize, sub_key: str, options: u32, access: u32, result: *u8) i32
```

access: KEY_READ=0x20019, KEY_WRITE=0x20006, KEY_ALL_ACCESS=0xF003F
result: pointer to HKEY output

### `reg_create_key_ex_a`

```quazi
pub fn reg_create_key_ex_a(key: usize, sub_key: str, reserved: u32, cls: str, options: u32, access: u32, security: *u8, result: *u8, disposition: *u32) i32
```

security: pointer to SECURITY_ATTRIBUTES or null
result: pointer to HKEY output; disposition: pointer to DWORD output (or null)

### `reg_close_key`

```quazi
pub fn reg_close_key(key: usize) i32
```

The Win32 function `RegCloseKey` (see its Microsoft documentation).

### `reg_query_value_ex_a`

```quazi
pub fn reg_query_value_ex_a(key: usize, value: str, reserved: *u32, reg_type: *u32, data: *u8, cb_data: *u32) i32
```

type: REG_SZ=1, REG_DWORD=4, REG_BINARY=3, REG_EXPAND_SZ=2, REG_MULTI_SZ=7
reserved/reg_type: pointer to DWORD (reserved must be null); data: pointer to value buffer
cb_data: pointer to DWORD (size in/out)

### `reg_set_value_ex_a`

```quazi
pub fn reg_set_value_ex_a(key: usize, value: str, reserved: u32, reg_type: u32, data: *u8, cb_data: u32) i32
```

data: pointer to value buffer to write

### `reg_delete_value_a`

```quazi
pub fn reg_delete_value_a(key: usize, value: str) i32
```

The Win32 function `RegDeleteValueA` (see its Microsoft documentation).

### `reg_delete_key_a`

```quazi
pub fn reg_delete_key_a(key: usize, sub_key: str) i32
```

The Win32 function `RegDeleteKeyA` (see its Microsoft documentation).

### `reg_enum_key_ex_a`

```quazi
pub fn reg_enum_key_ex_a(key: usize, index: u32, name: str, name_size: *u32, reserved: *u32, cls: str, cls_size: *u32, last_write: *u8) i32
```

name_size/cls_size: pointer to DWORD (in/out); reserved: pointer to DWORD (null)
last_write: pointer to FILETIME output

### `reg_enum_value_a`

```quazi
pub fn reg_enum_value_a(key: usize, index: u32, value: str, value_size: *u32, reserved: *u32, reg_type: *u32, data: *u8, data_size: *u32) i32
```

value_size/data_size: pointer to DWORD (in/out); reserved: pointer to DWORD (null)
reg_type: pointer to DWORD output; data: pointer to value buffer output

### `open_process_token`

```quazi
pub fn open_process_token(proc: usize, access: u32, token: *u8) i32
```

access: TOKEN_ADJUST_PRIVILEGES|TOKEN_QUERY=0x28
token: pointer to HANDLE output

### `open_thread_token`

```quazi
pub fn open_thread_token(thread: usize, access: u32, open_as_self: i32, token: *u8) i32
```

token: pointer to HANDLE output

### `lookup_privilege_value_a`

```quazi
pub fn lookup_privilege_value_a(system: str, name: str, luid: *u8) i32
```

luid: pointer to LUID struct (8 bytes) output

### `adjust_token_privileges`

```quazi
pub fn adjust_token_privileges(token: usize, disable_all: i32, new_state: *u8, buf_len: u32, prev: *u8, ret_len: *u32) i32
```

new_state/prev: pointer to TOKEN_PRIVILEGES struct; ret_len: pointer to DWORD output

### `get_token_information`

```quazi
pub fn get_token_information(token: usize, info_class: i32, info: *u8, info_len: u32, ret_len: *u32) i32
```

info: pointer to token information buffer; ret_len: pointer to DWORD output

### `is_user_an_admin`

```quazi
pub fn is_user_an_admin() i32
```

The Win32 function `IsUserAnAdmin` (see its Microsoft documentation).

### `get_system_info`

```quazi
pub fn get_system_info(si: *u8) void
```

si: pointer to SYSTEM_INFO struct output

### `get_native_system_info`

```quazi
pub fn get_native_system_info(si: *u8) void
```

The Win32 function `GetNativeSystemInfo` (see its Microsoft documentation).

### `global_memory_status_ex`

```quazi
pub fn global_memory_status_ex(stat: *u8) i32
```

stat: pointer to MEMORYSTATUSEX struct output (must set dwLength first)

### `get_computer_name_a`

```quazi
pub fn get_computer_name_a(buf: str, size: *u32) i32
```

The Win32 function `GetComputerNameA` (see its Microsoft documentation).

### `get_user_name_a`

```quazi
pub fn get_user_name_a(buf: str, size: *u32) i32
```

The Win32 function `GetUserNameA` (see its Microsoft documentation).

### `get_version_ex_a`

```quazi
pub fn get_version_ex_a(os_ver: *u8) i32
```

os_ver: pointer to OSVERSIONINFOEXA struct output (set dwOSVersionInfoSize first)

### `ws_startup`

```quazi
pub fn ws_startup(version: u16, data: *u8) i32
```

The Win32 function `WSAStartup` (see its Microsoft documentation).

### `ws_cleanup`

```quazi
pub fn ws_cleanup() i32
```

The Win32 function `WSACleanup` (see its Microsoft documentation).

### `ws_get_last_error`

```quazi
pub fn ws_get_last_error() i32
```

The Win32 function `WSAGetLastError` (see its Microsoft documentation).

### `socket`

```quazi
pub fn socket(af: i32, stype: i32, protocol: i32) usize
```

af: AF_INET=2, AF_INET6=23; type: SOCK_STREAM=1, SOCK_DGRAM=2; proto: IPPROTO_TCP=6

### `closesocket`

```quazi
pub fn closesocket(s: usize) i32
```

The Win32 function `closesocket` (see its Microsoft documentation).

### `bind`

```quazi
pub fn bind(s: usize, addr: *u8, addrlen: i32) i32
```

addr: pointer to sockaddr variant

### `listen`

```quazi
pub fn listen(s: usize, backlog: i32) i32
```

The Win32 function `listen` (see its Microsoft documentation).

### `accept`

```quazi
pub fn accept(s: usize, addr: *u8, addrlen: *i32) usize
```

addr: pointer to sockaddr output; addrlen: pointer to i32 (in/out)

### `connect`

```quazi
pub fn connect(s: usize, addr: *u8, addrlen: i32) i32
```

The Win32 function `connect` (see its Microsoft documentation).

### `send`

```quazi
pub fn send(s: usize, buf: *u8, len: i32, flags: i32) i32
```

The Win32 function `send` (see its Microsoft documentation).

### `recv`

```quazi
pub fn recv(s: usize, buf: *u8, len: i32, flags: i32) i32
```

The Win32 function `recv` (see its Microsoft documentation).

### `sendto`

```quazi
pub fn sendto(s: usize, buf: str, len: i32, flags: i32, to: *u8, tolen: i32) i32
```

to: pointer to destination sockaddr

### `recvfrom`

```quazi
pub fn recvfrom(s: usize, buf: str, len: i32, flags: i32, from: *u8, fromlen: *i32) i32
```

from: pointer to sockaddr output; fromlen: pointer to i32 (in/out)

### `setsockopt`

```quazi
pub fn setsockopt(s: usize, level: i32, optname: i32, optval: *u8, optlen: i32) i32
```

optval: pointer to option value buffer

### `getsockopt`

```quazi
pub fn getsockopt(s: usize, level: i32, optname: i32, optval: *u8, optlen: *i32) i32
```

optval: pointer to option value output; optlen: pointer to i32 (in/out)

### `getsockname`

```quazi
pub fn getsockname(s: usize, addr: *u8, addrlen: *i32) i32
```

addr: pointer to sockaddr output; addrlen: pointer to i32 (in/out)

### `getpeername`

```quazi
pub fn getpeername(s: usize, addr: *u8, addrlen: *i32) i32
```

The Win32 function `getpeername` (see its Microsoft documentation).

### `select`

```quazi
pub fn select(nfds: i32, readfds: *u8, writefds: *u8, exceptfds: *u8, timeout: *u8) i32
```

readfds/writefds/exceptfds: pointer to fd_set; timeout: pointer to TIMEVAL or null

### `ioctlsocket`

```quazi
pub fn ioctlsocket(s: usize, cmd: i32, argp: *u32) i32
```

argp: pointer to u_long output

### `getaddrinfo`

```quazi
pub fn getaddrinfo(node: str, service: str, hints: *u8, result: *u8) i32
```

hints: pointer to ADDRINFOA input; result: pointer to ADDRINFOA* output

### `freeaddrinfo`

```quazi
pub fn freeaddrinfo(info: *u8) void
```

info: pointer returned by getaddrinfo

### `getnameinfo`

```quazi
pub fn getnameinfo(addr: *u8, addrlen: i32, host: str, host_len: u32, serv: str, serv_len: u32, flags: i32) i32
```

The Win32 function `getnameinfo` (see its Microsoft documentation).

### `inet_pton`

```quazi
pub fn inet_pton(af: i32, src: str, dst: *u8) i32
```

dst: pointer to in_addr or in6_addr output

### `inet_ntop`

```quazi
pub fn inet_ntop(af: i32, src: *u8, dst: str, size: usize) str
```

src: pointer to in_addr or in6_addr input

### `htons`

```quazi
pub fn htons(hostshort: u16) u16
```

htons / ntohs — byte order conversion (no pointers)

### `ntohs`

```quazi
pub fn ntohs(netshort: u16) u16
```

The Win32 function `ntohs` (see its Microsoft documentation).

### `htonl`

```quazi
pub fn htonl(hostlong: u32) u32
```

The Win32 function `htonl` (see its Microsoft documentation).

### `ntohl`

```quazi
pub fn ntohl(netlong: u32) u32
```

The Win32 function `ntohl` (see its Microsoft documentation).
