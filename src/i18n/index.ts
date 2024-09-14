import { createI18n } from 'vue-i18n'
import { en } from './en'
import { zh } from './zh'

const i18n = createI18n({
    locale:  localStorage.getItem('locale') || 'zh',
    messages: {
        en, zh
    }
})

export default i18n