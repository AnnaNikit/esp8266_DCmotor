#define IS_SDL2 1
#define JAVA_NAMESPACE "org.kivy.android"
#define PY2 0
#define BOOTSTRAP "sdl2"
#define JNI_NAMESPACE "org/kivy/android"
JNIEnv *SDL_AndroidGetJNIEnv(void);
#define SDL_ANDROID_GetJNIEnv SDL_AndroidGetJNIEnv
