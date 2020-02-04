#define PY2 0
#define IS_SDL2 1
#define JNI_NAMESPACE "org/kivy/android"
#define JAVA_NAMESPACE "org.kivy.android"
#define BOOTSTRAP "sdl2"
JNIEnv *SDL_AndroidGetJNIEnv(void);
#define SDL_ANDROID_GetJNIEnv SDL_AndroidGetJNIEnv
