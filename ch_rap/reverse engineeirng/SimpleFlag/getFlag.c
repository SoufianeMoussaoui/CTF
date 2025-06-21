#include <stdio.h>
#include <string.h>

int getFlag(char* str){
	if (strcmp(str, "RS{c2luamFiX2hpZGRlbl9mbGFn}") == 0)
		return 1;
	return 0;
}
int main(){
	char str[64];
	printf("\n Entre the flag : ");
	scanf("%64s", str);
	if(getFlag(str))
		printf("\nThe flag is correct!!");
}