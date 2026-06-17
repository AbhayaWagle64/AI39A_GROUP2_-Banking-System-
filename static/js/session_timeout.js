// Session Timeout Manager for E-Paisa
// Location: static/js/session_timeout.js
// Auto-logout after 15min inactivity with 2min warning

class SessionManager {
    constructor(options = {}) {
        this.timeoutMinutes = options.timeoutMinutes || 15;
        this.warningMinutes = options.warningMinutes || 2;
        this.logoutUrl = options.logoutUrl || '/logout';
        this.pingUrl = options.pingUrl || '/api/ping';
        this.timeoutMs = this.timeoutMinutes * 60 * 1000;
        this.warningMs = this.warningMinutes * 60 * 1000;
        this.timer = null;
        this.warningTimer = null;
        this.isWarningShown = false;
        this.init();
    }

    init() {
        this.resetTimer();
        this.bindEvents();
        this.createWarningModal();
    }

    bindEvents() {
        const events = ['mousedown', 'mousemove', 'keypress', 'scroll', 'touchstart', 'click'];
        events.forEach(event => {
            document.addEventListener(event, () => this.resetTimer(), true);
        });
        setInterval(() => this.pingServer(), 5 * 60 * 1000);
    }

    resetTimer() {
        clearTimeout(this.timer);
        clearTimeout(this.warningTimer);
        this.isWarningShown = false;
        this.hideWarning();
        this.warningTimer = setTimeout(() => this.showWarning(), this.timeoutMs - this.warningMs);
        this.timer = setTimeout(() => this.logout(), this.timeoutMs);
    }

    createWarningModal() {
        if (document.getElementById('sessionWarningModal')) return;
        const modal = document.createElement('div');
        modal.id = 'sessionWarningModal';
        modal.className = 'hidden fixed inset-0 bg-black/80 backdrop-blur-sm z-[100] flex items-center justify-center p-4';
        modal.innerHTML = `
            <div class="bg-slate-900 border border-amber-500/30 rounded-2xl p-6 w-full max-w-sm text-center shadow-2xl">
                <div class="w-16 h-16 bg-amber-500/10 rounded-full flex items-center justify-center mx-auto mb-4">
                    <i class="fa-solid fa-clock text-amber-400 text-2xl"></i>
                </div>
                <h3 class="text-lg font-bold text-white mb-2">Session Expiring Soon</h3>
                <p class="text-slate-400 text-sm mb-4">You will be logged out in <span id="countdown" class="text-amber-400 font-bold font-mono">2:00</span> due to inactivity.</p>
                <div class="flex gap-3">
                    <button onclick="sessionManager.logout()" class="flex-1 bg-slate-800 text-slate-300 font-bold py-2.5 rounded-xl hover:bg-slate-700 transition text-sm">Logout Now</button>
                    <button onclick="sessionManager.stayLoggedIn()" class="flex-1 bg-emerald-500 text-white font-bold py-2.5 rounded-xl hover:bg-emerald-400 transition text-sm">Stay Logged In</button>
                </div>
            </div>
        `;
        document.body.appendChild(modal);
    }

    showWarning() {
        if (this.isWarningShown) return;
        this.isWarningShown = true;
        const modal = document.getElementById('sessionWarningModal');
        modal.classList.remove('hidden');
        let seconds = this.warningMinutes * 60;
        this.countdownInterval = setInterval(() => {
            seconds--;
            const mins = Math.floor(seconds / 60);
            const secs = seconds % 60;
            const el = document.getElementById('countdown');
            if (el) el.textContent = `${mins}:${secs.toString().padStart(2, '0')}`;
            if (seconds <= 0) { clearInterval(this.countdownInterval); this.logout(); }
        }, 1000);
    }

    hideWarning() {
        const modal = document.getElementById('sessionWarningModal');
        if (modal) modal.classList.add('hidden');
        if (this.countdownInterval) clearInterval(this.countdownInterval);
    }

    stayLoggedIn() {
        this.hideWarning();
        this.resetTimer();
        this.pingServer();
    }

    async pingServer() {
        try { await fetch(this.pingUrl, { method: 'POST', credentials: 'same-origin' }); }
        catch (e) { console.log('Ping failed'); }
    }

    logout() {
        clearTimeout(this.timer);
        clearTimeout(this.warningTimer);
        if (this.countdownInterval) clearInterval(this.countdownInterval);
        const msg = document.createElement('div');
        msg.className = 'fixed inset-0 bg-slate-950 z-[200] flex items-center justify-center';
        msg.innerHTML = `
            <div class="text-center">
                <div class="w-16 h-16 bg-rose-500/10 rounded-full flex items-center justify-center mx-auto mb-4 animate-pulse">
                    <i class="fa-solid fa-lock text-rose-400 text-2xl"></i>
                </div>
                <h3 class="text-xl font-bold text-white mb-2">Session Expired</h3>
                <p class="text-slate-400 text-sm">You have been logged out for security.</p>
            </div>
        `;
        document.body.appendChild(msg);
        setTimeout(() => { window.location.href = this.logoutUrl; }, 2000);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    window.sessionManager = new SessionManager({ timeoutMinutes: 15, warningMinutes: 2 });
});