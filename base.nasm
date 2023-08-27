global _start     ; global is used to export the _start label.
                  ; This will be the entry point to the program.

section .data
    dat times {length} db 0

;ecx = index
;r11 = value
section .text
move_left: ; <
    cmp ecx, dat
    jne normal_left
    mov ecx, dat+{length-1}
    ret

    normal_left:
        dec ecx
    ret

move_right: ; >
    cmp ecx, dat+{length-1}
    jne normal_right
    mov ecx, dat
    ret

    normal_right:
        inc ecx
    ret

increment: ; +
    mov al, byte [ecx]
    inc al
    mov byte [ecx], al
    ret

decrement: ; -
    mov al, byte [ecx]
    dec al
    mov byte [ecx], al
    ret

print: ; .
    ;location of char to print is ecx
    ;######################################
    ; syscall - write(1, msg, len);
    ;######################################
    mov eax, 4     ; 4 = Syscall number for Write()
    mov ebx, 1     ; File Descriptor to write to
                   ; In this case: STDOUT is 1
    mov edx, 1     ; The length of string to print
                   ; which is 1 character
    int 0x80       ; Poke the kernel and tell it to run the
                   ; write() call we set up
    ret

read: ; ,
    mov eax, 3          ; Syscall number for read
    mov ebx, 0          ; stdin?
    mov edx, 1          ; | <- length
    int 80h             
    ret

exit:
    ;######################################
    ; syscall - exit(0);
    ;######################################
    mov al, 1      ; Syscall for Exit()
    int 0x80       ; Poke kernel. This will end the program
    ret

_start:
    mov ecx, dat
{asm}

    mov ebx, 0     ; The status code we want to provide.
    call exit
