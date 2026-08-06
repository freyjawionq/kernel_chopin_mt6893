#ifndef __KSU_H_MANAGER_IDENTITY
#define __KSU_H_MANAGER_IDENTITY

#define KSU_INVALID_APPID -1
#define KSU_PER_USER_RANGE 100000
#define KSU_MAX_MANAGERS 16

struct ksu_manager_entry {
	uid_t uid;
	char pkg[KSU_MAX_PACKAGE_NAME];
	u32 version;
};

extern struct ksu_manager_entry ksu_managers[KSU_MAX_MANAGERS];
extern int ksu_manager_count;

static inline bool ksu_is_manager_appid_valid(void)
{
	return ksu_manager_count > 0;
}

static inline bool is_manager(void)
{
	uid_t current_appid = current_uid().val % KSU_PER_USER_RANGE;
	int i;
	for (i = 0; i < ksu_manager_count; i++) {
		if (ksu_managers[i].uid == current_appid)
			return true;
	}
	return false;
}

static inline bool is_uid_manager(uid_t uid)
{
	uid_t appid = uid % KSU_PER_USER_RANGE;
	int i;
	for (i = 0; i < ksu_manager_count; i++) {
		if (ksu_managers[i].uid == appid)
			return true;
	}
	return false;
}

static inline uid_t ksu_get_manager_appid(void)
{
	return ksu_manager_count > 0 ? ksu_managers[0].uid : KSU_INVALID_APPID;
}

static inline u32 ksu_get_manager_version_for_current(u32 default_version)
{
	uid_t current_appid = current_uid().val % KSU_PER_USER_RANGE;
	int i;
	for (i = 0; i < ksu_manager_count; i++) {
		if (ksu_managers[i].uid == current_appid) {
			if (ksu_managers[i].version != 0)
				return ksu_managers[i].version;
		}
	}
	return default_version;
}

static inline void ksu_register_manager(uid_t appid, const char *pkg)
{
	int i;
	for (i = 0; i < ksu_manager_count; i++) {
		if (ksu_managers[i].uid == appid)
			return;
	}
	if (ksu_manager_count < KSU_MAX_MANAGERS) {
		ksu_managers[ksu_manager_count].uid = appid;
		if (pkg) {
			strncpy(ksu_managers[ksu_manager_count].pkg, pkg, KSU_MAX_PACKAGE_NAME - 1);
			ksu_managers[ksu_manager_count].pkg[KSU_MAX_PACKAGE_NAME - 1] = '\0';

			if (!strcmp(pkg, "com.rifsxd.ksunext")) {
				ksu_managers[ksu_manager_count].version = 33188;
			} else if (!strcmp(pkg, "com.resukisu.resukisu")) {
				ksu_managers[ksu_manager_count].version = 35052;
			} else if (!strcmp(pkg, "com.kow712.kowsu") || !strcmp(pkg, "com.kowx712.supermanager")) {
				ksu_managers[ksu_manager_count].version = 35052;
			} else if (!strcmp(pkg, "me.weishu.kernelsu")) {
				ksu_managers[ksu_manager_count].version = 32567;
			} else {
				ksu_managers[ksu_manager_count].version = 35052;
			}
		} else {
			ksu_managers[ksu_manager_count].pkg[0] = '\0';
			ksu_managers[ksu_manager_count].version = 35052;
		}
		ksu_manager_count++;
	}
}

static inline void ksu_set_manager_appid(uid_t appid)
{
	ksu_register_manager(appid, NULL);
}

static inline void ksu_invalidate_manager_uid(void)
{
	ksu_manager_count = 0;
}

#endif


