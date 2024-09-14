import { defineStore } from 'pinia';

export const useLanguageStore = defineStore('language', {
  state: () => ({
    locale: localStorage.getItem('locale') || 'zh'
  }),
  actions: {
    setLocale(locale: string) {
      this.locale = locale;
      localStorage.setItem('locale', locale);
    }
  }
});