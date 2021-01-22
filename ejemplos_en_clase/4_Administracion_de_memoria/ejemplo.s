	.file	"ejemplo.c"
	.text
	.globl	var1
	.data
	.align 4
	.type	var1, @object
	.size	var1, 4
var1:
	.long	10
	.section	.rodata
	.align 8
.LC0:
	.string	"\302\241Hola mundo! Mis variables son %d y %d.\n"
	.text
	.globl	main
	.type	main, @function
main:
.LFB0:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$16, %rsp
	movl	$20, -4(%rbp)
	movl	var1(%rip), %eax
	movl	-4(%rbp), %edx
	movl	%eax, %esi
	leaq	.LC0(%rip), %rdi
	movl	$0, %eax
	call	printf@PLT
	nop
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE0:
	.size	main, .-main
	.ident	"GCC: (Debian 10.2.1-3) 10.2.1 20201224"
	.section	.note.GNU-stack,"",@progbits
