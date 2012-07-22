#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>


int main (int argc, char **argv) {
  int i, j;

  if ( argc != 3 ) {
    printf("Usage: truncate FILE1 numbytes\n");
    return -1;
  }
  FILE *file1 = fopen(argv[1], "wb");
  if (file1 < 0 ) {
    printf("error opening file\n");
    return -1;
  }

  int truncsize =  atoi(argv[2]);
  ftruncate(fileno(file1), truncsize);  
  fclose(file1);
  
  return 0;
}
