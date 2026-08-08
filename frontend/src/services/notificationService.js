class NotificationService {
  constructor() {
    this.listeners = [];
  }

  subscribe(listener) {
    this.listeners.push(listener);
    return () => {
      this.listeners = this.listeners.filter((l) => l !== listener);
    };
  }

  notify(message, type = 'info') {
    const payload = { message, type, id: Date.now() };
    this.listeners.forEach((l) => l(payload));
  }

  success(message) {
    this.notify(message, 'success');
  }

  error(message) {
    this.notify(message, 'error');
  }

  warning(message) {
    this.notify(message, 'warning');
  }

  info(message) {
    this.notify(message, 'info');
  }
}

export const notificationService = new NotificationService();
