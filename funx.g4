grammar funx;

root : function* expr? EOF; 


instr: assign
    |ifcondition
    |elsecondition
    |whilecondition
    |expr
    ;

expr : PARA expr PARC #Par
    | <assoc=right> expr POW expr #Arith
    | expr (MUL|DIV|MOD) expr #Arith
    | expr (MES|RES) expr #Arith
    | functioncall #cridaF
    | VAR # Var
    | NUM # Valor
    ;

 
function: FUNCTION expr* CLAUDATORA instr* CLAUDATORC;

assign:  VAR ASSIGN expr;

ifcondition: IF condition CLAUDATORA instr* CLAUDATORC (elsecondition)?;

elsecondition: ELSE CLAUDATORA instr* CLAUDATORC;

condition: expr (MENORI|MENOR|MAYORI|MAYOR|IGUAL|NIGUAL) expr;

functioncall: FUNCTION expr*;

whilecondition: WHILE condition CLAUDATORA instr* CLAUDATORC;

PARA : '(';
PARC : ')';
CLAUDATORA: '{';
CLAUDATORC: '}';
MES : '+';
RES : '-';
MUL : '*';
DIV : '/';
MOD: '%';
POW : '**';
ASSIGN: '<-';
WRITE: 'write';
IF: 'if';
ELSE: 'else';
WHILE: 'while';
DO: 'do';
MENORI: '<=';
MENOR: '<';
MAYORI: '>=';
MAYOR: '>';
IGUAL: '=';
NIGUAL: '!=';

COMENTARY: ('#' ~[\r\n]*)+ -> skip;

FUNCTION: [A-Z] [a-zA-Z\u0080-\u00FF0-9_]*;
NUM : [0-9]+;
VAR : [a-z] [a-zA-Z\u0080-\u00FF0-9]*;
WS : [ \t\r\n]+ -> skip ;

unknowns: Unknown+ ;

Unknown: . ;
