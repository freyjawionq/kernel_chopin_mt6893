#ifndef __KSU_H_APK_V2_SIGN
#define __KSU_H_APK_V2_SIGN

bool is_manager_apk(char *path);
enum ksu_manager_profile {
	KSU_MANAGER_OFFICIAL = 0,
	KSU_MANAGER_KOWSU,
	KSU_MANAGER_NEXT,
	KSU_MANAGER_RESUKISU,
};
enum ksu_manager_profile get_manager_profile(char *path);
int get_pkg_from_apk_path(char *pkg, const char *path);

#endif
