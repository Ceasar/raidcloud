#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>

int getfilesize(FILE *f) {
  int fd = fileno(f);
  struct stat buf;
  fstat(fd, &buf);
  int size = buf.st_size;
  return size;
}

int main (int argc, char **argv) {
  int i, j;

  if ( argc != 3 ) {
    printf("Usage: fileparity FILE1 FILE2\n");
    return -1;
  }
  FILE *file1 = fopen(argv[1], "r");
  if (file1 < 0) {
    printf("error opening file\n");
    return -1;
  }
  FILE *file2 = fopen(argv[2], "r");
  if (file1 < 0) {
    printf("error opening file\n");
    return -1;
  }
  // These files better be the same size
    
  int filesize1 = getfilesize(file1);
  int filesize2 = getfilesize(file2);
  if ( filesize1 != filesize2 ) {
    printf("error: files aren't the same size\n");
    printf("exiting\n");
    return -1;
  }

  // okay, let's go
  char c1 = fgetc(file1);
  char c2 = fgetc(file2);
  while (!feof(file1) && !feof(file2)) {
    printf("%c",(c1^c2));
    c1 = fgetc(file1);
    c2 = fgetc(file2);
  }
  return 0;
}
