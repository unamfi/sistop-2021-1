%{
#include<stdio.h>
%}

%option yylineno
%option noyywrap

letra [a-zA-Z]
num [0-9]
stdio [fopen,remove,fflush,fgets,fputs,printf,puts]

%%

int|float|char|double|boolean|tolower|if|else|switch|do|while|void|for|short|case|break|long|default|continue|sizeof|typedef  {printf("%s Es palabra reservada",yytext);}
{stdio}+ {printf("%s Es una funcion que pertenece a la bliblioteca <stdio.h>",yytext);} //Expresion regular que reconoce la cadena como funcion
(_|{letra})(_|{letra}|{num})*  {printf("%s Es un identificador",yytext);} //Expresion regular que reconoce la cadena como identificador
.* {printf("Cadena no valida %s",yytext);} //Aqui se reconoce cualquier otra cadena que no sea de los arriba

%%
void main(int argc, char *cad[]){
if(argc>1)
yyin=fopen(cad[1],"r");
else{
printf("Error 404 FILE NOT FOUND");
exit(0);
}
yylex();
}