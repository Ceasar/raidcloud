#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>


int main (int argc, char **argv) {
  int i, j;

  if ( argc != 2 ) {
    printf("Usage: autotrunc FILE\n");
    return -1;
  }
  FILE *file1 = fopen(argv[1], "r+b");
  if (file1 < 0 ) {
    printf("error opening file\n");
    return -1;
  }
  
  fseek(file1,-1,SEEK_END);
  printf("ftell: %ld\n",ftell(file1));
  int count = 0;
  char c = fgetc(file1);
  printf("%c found\n",c);
  int pads = atoi(&c);
  if (pads > 0) {
    fseek(file1,-pads,SEEK_END);
    ftruncate(fileno(file1), ftell(file1));
  }
  fclose(file1);
  printf("Truncated %d bytes\n",pads);
  return 0;
}
