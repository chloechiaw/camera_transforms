For the prototype version, the Regex consists of uppercase English letters, “[“, and “]” here a string if characters enclosed in square brackets “[“ and “]” matches any of the one characters in that string, also the string of characters enclosed within [ nad ] consists of uppercase English letters only with no repetition. 
for example 
[AABR]ABC is not a valid regez as b occurs twice between square brackets 

"[]ABC", "A[A][",]" is not valid as brackets must contain some string 

"[ABC]BC[A]" is a valid regex and matches with "BBCA" and "ABCA" but not with "ABBCA"
"[ABCZ][Q]" is a valid regex and matches with "AQ", "BQ", "CQ", "ZQ" but nt with DQ AND ZC.ZeroDivisionError
given three strings x y z of length n, find the longest regex that matches both the strings x and y but does not match with the string z. if no such regex exists output -1. if multiple such regexes exist output the lexigographically smallest one. 