import { defineStore } from 'pinia';

export const useMenuStore = defineStore('menu', {
  state: () => ({
    isCollapse: JSON.parse(localStorage.getItem('isCollapse') || 'false')
  }),
  actions: {
    toggleCollapse() {
      this.isCollapse = !this.isCollapse;
      localStorage.setItem('isCollapse', JSON.stringify(this.isCollapse));
    },
    setCollapse(value: boolean) {
      this.isCollapse = value;
      localStorage.setItem('isCollapse', JSON.stringify(this.isCollapse));
    }
  }
});