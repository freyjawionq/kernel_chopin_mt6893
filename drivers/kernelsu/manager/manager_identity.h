#ifndef __KSU_H_MANAGER_IDENTITY
#define __KSU_H_MANAGER_IDENTITY

#define KSU_INVALID_APPID -1
#define KSU_PER_USER_RANGE 100000
#define KSU_MAX_MANAGERS 16

extern uid_t ksu_manager_appids[KSU_MAX_MANAGERS];
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
		if (ksu_manager_appids[i] == current_appid)
			return true;
	}
	return false;
}

static inline bool is_uid_manager(uid_t uid)
{
	uid_t appid = uid % KSU_PER_USER_RANGE;
	int i;
	for (i = 0; i < ksu_manager_count; i++) {
		if (ksu_manager_appids[i] == appid)
			return true;
	}
	return false;
}

static inline uid_t ksu_get_manager_appid(void)
{
	return ksu_manager_count > 0 ? ksu_manager_appids[0] : KSU_INVALID_APPID;
}

static inline void ksu_set_manager_appid(uid_t appid)
{
	int i;
	for (i = 0; i < ksu_manager_count; i++) {
		if (ksu_manager_appids[i] == appid)
			return;
	}
	if (ksu_manager_count < KSU_MAX_MANAGERS) {
		ksu_manager_appids[ksu_manager_count++] = appid;
	}
}

static inline void ksu_invalidate_manager_uid(void)
{
	ksu_manager_count = 0;
}

#endif

