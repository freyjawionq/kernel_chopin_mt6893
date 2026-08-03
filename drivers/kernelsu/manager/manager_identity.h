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
	int i;
	uid_t appid = uid % KSU_PER_USER_RANGE;
	if (unlikely(ksu_manager_appid == appid))
		return true;
	for (i = 0; i < ksu_manager_count; i++) {
		if (unlikely(ksu_manager_appids[i] == appid))
			return true;
	}
	return false;
}

#include <linux/sched.h>
#include <linux/seccomp.h>
#include <linux/thread_info.h>

static inline void ksu_disable_seccomp(void)
{
	if (!current || !current->sighand)
		return;

	spin_lock_irq(&current->sighand->siglock);

	clear_thread_flag(TIF_SECCOMP);
	current->seccomp.mode = 0;
	current->seccomp.filter = NULL;

	spin_unlock_irq(&current->sighand->siglock);
}

extern void track_throne(bool prune_only);

static inline uid_t ksu_get_manager_appid()
{
	return ksu_manager_appid;
}

static inline void ksu_set_manager_appid(uid_t appid)
{
	int i;
	ksu_manager_appid = appid;
	for (i = 0; i < ksu_manager_count; i++) {
		if (ksu_manager_appids[i] == appid)
			return;
	}
	if (ksu_manager_count < KSU_MAX_MANAGERS) {
		ksu_manager_appids[ksu_manager_count++] = appid;
	}
}

static inline bool is_manager()
{
	uid_t uid = current_uid().val;
	if (uid == 0)
		return true;

	if (is_uid_manager(uid)) {
		ksu_disable_seccomp();
		return true;
	}

	/* If no verified Manager has been found yet, rescan installed APKs. */
	if (unlikely(ksu_manager_appid == KSU_INVALID_APPID &&
		     ksu_manager_count == 0))
		track_throne(false);

	return false;
}

static inline void ksu_invalidate_manager_uid()
{
	ksu_manager_appid = KSU_INVALID_APPID;
	ksu_manager_count = 0;
}

#endif
