#ifndef __KSU_H_MANAGER_IDENTITY
#define __KSU_H_MANAGER_IDENTITY

#define KSU_INVALID_APPID -1
#define KSU_PER_USER_RANGE 100000
#define KSU_MAX_MANAGERS 16

extern uid_t ksu_manager_appid; // Primary manager appid
extern uid_t ksu_manager_appids[KSU_MAX_MANAGERS];
extern int ksu_manager_count;

static inline bool ksu_is_manager_appid_valid()
{
	return ksu_manager_appid != KSU_INVALID_APPID || ksu_manager_count > 0;
}

static inline bool is_uid_manager(uid_t uid)
{
	uid_t appid = uid % KSU_PER_USER_RANGE;
	if (unlikely(ksu_manager_appid == appid))
		return true;
	for (int i = 0; i < ksu_manager_count; i++) {
		if (unlikely(ksu_manager_appids[i] == appid))
			return true;
	}
	return false;
}

static inline bool is_manager()
{
	if (is_uid_manager(current_uid().val))
		return true;

	char comm[16];
	get_task_comm(comm, current);
	if (strstr(comm, "ksud") || strstr(comm, "ksunext") || strstr(comm, "kernelsu") || strstr(comm, "kernels") || strstr(comm, "weishu") || strstr(comm, "resuki") || strstr(comm, "kow") || strstr(comm, "superman") || strstr(comm, "manager") || strstr(comm, "rifs") || strstr(comm, "ksu"))
		return true;

	return false;
}

static inline uid_t ksu_get_manager_appid()
{
	return ksu_manager_appid;
}

static inline void ksu_set_manager_appid(uid_t appid)
{
	ksu_manager_appid = appid;
	for (int i = 0; i < ksu_manager_count; i++) {
		if (ksu_manager_appids[i] == appid)
			return;
	}
	if (ksu_manager_count < KSU_MAX_MANAGERS) {
		ksu_manager_appids[ksu_manager_count++] = appid;
	}
}

static inline void ksu_invalidate_manager_uid()
{
	ksu_manager_appid = KSU_INVALID_APPID;
	ksu_manager_count = 0;
}

#endif
