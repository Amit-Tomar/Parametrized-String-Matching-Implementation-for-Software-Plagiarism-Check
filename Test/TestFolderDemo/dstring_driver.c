/*
* Author: Sandeep K
* Date: July-30-2013
* Description: Testing Driver for dstring library. Tests all functionality of dstring.
*/

#include "dstring.h"
#include<stdio.h>
#include<stdlib.h>
#include<string.h>

int main(int argc, char** argv){	
	int i = 0, flag = 1, total_testcases=16, pass_count = 0, fail_count=0;	
	
	// Data to test dstring create
	char* create_in1 = "Testing dstrcreate 1";
	char* create_in2 = "";
	
	dstring* create_din1 = NULL;
	dstring* create_din2 =  NULL;
	
	// Data to test dstring copy
	dstring* copy_src1 = dstrcreate("Testing dstrcopy 1",18 );
	dstring* copy_src2 = dstrcreate("",0);
	dstring* copy_dest1 = dstrcreate("Should be removed",17);
	dstring* copy_dest2 = dstrcreate("",0);
	
	// Data to test dstring concatenate
	dstring* concat_src1 = dstrcreate("",0);
	dstring* concat_src2 = dstrcreate("First part,",11);
	dstring* concat_src3 = dstrcreate("First part, ", 12);
	dstring* concat_dest1 = dstrcreate("Second part.",12);
	dstring* concat_dest2 = dstrcreate(" Second part.", 13);
	
	char* expected_output1 = "Second part.";
	char* expected_output2 = "First part, Second part.";
	char* expected_output3 = "First part, Second part.";
	
	// Data to test dstring length
	dstring* len_str1 = dstrcreate("",0);
	dstring* len_str2 = dstrcreate("one", 3);
	
	// Data to test dstring compare
	dstring* cmp_str1_case1 = dstrcreate(" ",1);
	dstring* cmp_str2_case1 = dstrcreate("",0);
	int expected_case1 = 1; 
	
	dstring* cmp_str1_case2 = dstrcreate("we are equal",12);
	dstring* cmp_str2_case2 = dstrcreate("we are equal",12);
	int expected_case2 = 0; 
	
	dstring* cmp_str1_case3 = dstrcreate("Greaterrr",9);
	dstring* cmp_str2_case3 = dstrcreate("Greaterr",8);
	int expected_case3 = 1; 
	
	dstring* cmp_str1_case4 = dstrcreate("smaller",7);
	dstring* cmp_str2_case4 = dstrcreate("smallerr",8);
	int expected_case4 = -1; 
	
	dstring* cmp_str1_case5 = dstrcreate("a",1);
	dstring* cmp_str2_case5 = dstrcreate("b",8);
	int expected_case5 = -1; 
	
	// Test dstrcreate
	printf("\n\n--------------- Testing dstrcreate() ----------------\n\n");
	
	create_din1 = dstrcreate(create_in1, 20);
	flag = 1;
	for(i=0; i<20; i++){
		if(create_din1->buf[i] != create_in1[i]){
			flag = -1;
			break;
		}
	}
	
	if(flag == -1){
		fail_count++;
		printf("ERROR: dstrcreate() - Test case 1\n");
	}
	else{
		pass_count++;
		printf("SUCCESS: dstrcreate() - Test case 1\n");
	}
	
	if(create_din1->length != 20){
		fail_count++;
		printf("ERROR: dstrcreate() - Test case 2\n");
	}else{
		pass_count++;
		printf("SUCCESS: dstrcreate() - Test case 2\n");
	}
	
	create_din2 = dstrcreate(create_in2, 0);
	
	if(create_din2->buf == NULL){
		fail_count++;
		printf("ERROR: dstrcreate() - Test case 3\n");
	}
	else{
		pass_count++;
		printf("SUCCESS: dstrcreate() - Test case 3\n");
	}
	
	if(create_din2->length != 0){
		fail_count++;
		printf("ERROR: dstrcreate() - Test case 4\n");
	}
	else{
		pass_count++;
		printf("SUCCESS: dstrcreate() - Test case 4\n");
	}
		
	// Test dstrcpy
	printf("\n\n--------------- Testing dstrcpy() ----------------\n\n");

	copy_dest1 = dstrcpy(copy_dest1, copy_src1);

	flag = 1;
    if(copy_dest1->length != copy_src1->length)
        flag = -1;
	
    for(i=0;i<copy_src1->length; i++){
        if(copy_dest1->buf[i] != copy_src1->buf[i])
            flag = -1;
    }
	
	if(flag == -1){
		fail_count++;
		printf("ERROR: dstrcpy() - Test case 5\n");
	}else{
		pass_count++;
		printf("SUCCESS: dstrcpy() - Test case 5\n");
	}
	
	copy_dest2 = dstrcpy(copy_dest2, copy_src2);
	
	flag = 1;
	if(copy_dest2->length != copy_src2->length)
		flag = -1;
	
	for(i=0;i<copy_src2->length; i++){
		if(copy_dest2->buf[i] != copy_src2->buf[i])
			flag = -1;
	}
	
	if(flag == -1){
		fail_count++;
		printf("ERROR: dstrcpy() - Test case 6\n");
	}else{
		pass_count++;
		printf("SUCCESS: dstrcpy() - Test case 6\n");
	}
	
	// Test dstrcat
	printf("\n\n--------------- Testing dstrcat() ----------------\n\n");

	concat_src1 = dstrcat(concat_src1, concat_dest1);
	flag = 1;
	if(concat_src1->length != 12){
		flag = -1;
	}
	
	for(i=0;i<strlen(expected_output1);i++){
		if(concat_src1->buf[i] != expected_output1[i])
			flag = -1;
	}
	
	if(flag == -1){
		fail_count++;
		printf("ERROR: dstrcat() - Test case 7\n");
	}else{
		pass_count++;
		printf("SUCCESS: dstrcat() - Test case 7\n");
	}
	
	concat_src2 = dstrcat(concat_src2, concat_dest2);
	flag = 1;
	if(concat_src2->length != 24){
		flag = -1;
	}
	
	for(i=0;i<strlen(expected_output2);i++){
		if(concat_src2->buf[i] != expected_output2[i]){
			flag = -1;
		}
	}
	
	if(flag == -1){
		fail_count++;
		printf("ERROR: dstrcat() - Test case 8\n");
	}else{
		pass_count++;
		printf("SUCCESS: dstrcat() - Test case 8\n");
	}
	
	concat_src3 = dstrcat(concat_src3, concat_dest1);
	flag = 1;
	if(concat_src3->length != 24){
		flag = -1;
	}
	
	for(i=0;i<strlen(expected_output3);i++){
		if(concat_src3->buf[i] != expected_output3[i])
			flag = -1;
	}
	
	if(flag == -1){
		fail_count++;
		printf("ERROR: dstrcat() - Test case 9\n");
	}else{
		pass_count++;
		printf("SUCCESS: dstrcat() - Test case 9\n");
	}
	
	// Test dstrlen
	printf("\n\n--------------- Testing dstrlen() ----------------\n\n");
	
	if(len_str1->length == 0){
		pass_count++;
		printf("SUCCESS: dstrlen() - Test case 10\n");
	}
	else{
		printf("ERROR: dstrlen() - Test case 10\n");
		fail_count++;
	}

	if(len_str2->length == 3){
		pass_count++;
		printf("SUCCESS: dstrlen() - Test case 11\n");
	}
	else{
		printf("ERROR: dstrlen() - Test case 11\n");
		fail_count++;
	}
	
	// Test dstrcmp
	printf("\n\n--------------- Testing dstrcmp() ----------------\n\n");
	
	if(dstrcmp(cmp_str1_case1, cmp_str2_case1) == expected_case1){
		pass_count++;
		printf("SUCCESS: dstrcmp() - Test case 12\n");
	}else{
		fail_count++;
		printf("ERROR: dstrcmp() - Test case 12\n");
	}
	
	if(dstrcmp(cmp_str1_case2, cmp_str2_case2) == expected_case2){
		pass_count++;
		printf("SUCCESS: dstrcmp() - Test case 13\n");
	}else{
		fail_count++;
		printf("ERROR: dstrcmp() - Test case 13\n");
	}	
	
	if(dstrcmp(cmp_str1_case3, cmp_str2_case3) == expected_case3){
		pass_count++;
		printf("SUCCESS: dstrcmp() - Test case 14\n");
	}else{
		fail_count++;
		printf("ERROR: dstrcmp() - Test case 14\n");
	}
	
	if(dstrcmp(cmp_str1_case4, cmp_str2_case4) == expected_case4){
		pass_count++;
		printf("SUCCESS: dstrcmp() - Test case 15\n");
	}else{
		fail_count++;
		printf("ERROR: dstrcmp() - Test case 15\n");
	}
	
	if(dstrcmp(cmp_str1_case5, cmp_str2_case5) == expected_case5){
		pass_count++;
		printf("SUCCESS: dstrcmp() - Test case 16\n");
	}else{
		fail_count++;
		printf("ERROR: dstrcmp() - Test case 16\n");
	}
	
	// Test dstrfree
	printf("\n\n--------------- Testing dstrfree() ----------------\n\n");
	
	dstrfree(create_din1);
	dstrfree(create_din2);
	dstrfree(copy_src1);
	dstrfree(copy_src2);
	dstrfree(copy_dest1);
	dstrfree(copy_dest2);
	dstrfree(concat_src1);
	dstrfree(concat_src2);
	dstrfree(concat_src3);
	dstrfree(concat_dest1);
	dstrfree(concat_dest2);
	dstrfree(len_str1);
	dstrfree(len_str2);
	dstrfree(cmp_str1_case1);
	dstrfree(cmp_str1_case2);
	dstrfree(cmp_str1_case3);
	dstrfree(cmp_str1_case4);
	dstrfree(cmp_str1_case5);
	dstrfree(cmp_str2_case1);
	dstrfree(cmp_str2_case2);
	dstrfree(cmp_str2_case3);
	dstrfree(cmp_str2_case4);
	dstrfree(cmp_str2_case5);
	
	printf("\n\n------------ Summary --------------\n\n");
	
	printf("Total test cases : %d\n", total_testcases);
	printf("Successful test cases: %d\n", pass_count);
	printf("Failed test cases: %d\n", fail_count);	
}
