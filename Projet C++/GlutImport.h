#ifdef __linux__ 
extern "C"
{
   #include <GL/glut.h>
}
#endif

#ifdef  _WIN32
#include "glut.h" 
#endif


#ifdef __APPLE__
#include "GLUT/glut.h"
#endif
