section .data
    message db "Hello World", 10, 0 ; Null terminated string

section .text

global _start
_start:
    mov rax, 1
    mov rdi, 1
    mov rsi, message
    mov rdx, 0
    count:
        cmp byte [rsi + rdx], 0
        je done
        inc rdx
        jmp count
    done:
        syscall
        
    mov rax, 60
    mov rdi, 0
    syscall