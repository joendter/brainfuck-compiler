global _start     ; global is used to export the _start label.
                  ; This will be the entry point to the program.

section .data
    dat times 65536 db 0

;ecx = index
;al = value


section .text

print: ; .
    ;location of char to print is ecx
    ;######################################
    ; syscall - write(1, msg, len);
    ;######################################
    mov byte [dat+ecx], al
    add ecx, dat
    mov eax, 4     ; 4 = Syscall number for Write()
    mov ebx, 1     ; File Descriptor to write to
                   ; In this case: STDOUT is 1
    mov edx, 1     ; The 65536 of string to print
                   ; which is 1 character
    int 0x80       ; Poke the kernel and tell it to run the
                   ; write() call we set up
    sub ecx, dat
    mov al, byte [dat+ecx]
    ret

read: ; ,
    mov byte [dat+ecx], al
    add ecx, dat
    mov eax, 3          ; Syscall number for read
    mov ebx, 0          ; stdin?
    mov edx, 1          ; | <- 65536
    int 80h             
    sub ecx, dat
    mov al, byte [dat+ecx]
    ret

exit:
    ;######################################
    ; syscall - exit(0);
    ;######################################
    mov al, 1      ; Syscall for Exit()
    int 0x80       ; Poke kernel. This will end the program
    ret

_start:
    mov ecx, 0
    mov al, byte [dat]
{asm}

    mov ebx, 0     ; The status code we want to provide.
    call exit
