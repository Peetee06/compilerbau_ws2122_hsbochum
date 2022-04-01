# compilerbau_ws2122_hsbochum
This repository contains the code of the compiler created for module Compilerbau at Hochschule Bochum in Wintersemester 2021/2022 by Khaled Youssef, Henning Nolte and Peter Trost.

Die Grammatik unserer Programmiersprache ist folgendermaßen nach der w3 Definition der Notation von Syntax (https://www.w3.org/Notation.html) definiert:    

``` 
Program ::= *(Instruction | Function)
  
Instruction ::= While  
			| Ifelse  
			| Expression";"  
			| ID "=" Expression";"  
  
Function ::= "def" ID "(" [*(Arg ",")Arg] ")" "{" Instruction "}"  
  
While ::= "while" "(" Boolexpr ")" "{" Instruction "}"  
  
Ifelse ::= "If" "(" Boolexpr ")" "{" Instruction "}" ["else" "{" Instruction "}"]  
  
Expression ::= Term | Boolexpr | """ [String] """ | ID "(" [*((ID|Num|String),) (ID|Num|String)] ")" ";"  
  
Boolexpr ::= "(" Boolexpr ")" | Boolexpr ("and" | "or") Boolexpr | "not" Boolexpr | Comparison | "1" | "0"  
  
Comparison ::= Term ("==" | "<=" | ">=" | "!=" | "<" | ">") Term  
  
Term ::= "(" Term ")" | (Term | Num) ("+" | "-" | "*" | "/") (Term | Num)  
  
String ::= <any character>  
  
Num ::= PosNum *Digit ["." *Digit] | Digit  
  
Digit -> "0" | PosNum  
  
PosNum -> "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"  
```