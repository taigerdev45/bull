export default defineNuxtPlugin(() => {
  if (process.client) {
    const originalAddEventListener = window.EventTarget.prototype.addEventListener
    window.EventTarget.prototype.addEventListener = function (type, listener, options) {
      let modOptions = options
      if (['touchstart', 'touchmove', 'wheel', 'mousewheel'].includes(type)) {
        if (typeof options === 'boolean') {
          modOptions = { capture: options, passive: true }
        } else if (typeof options === 'object' && options !== null) {
          modOptions = { ...options, passive: options.passive !== undefined ? options.passive : true }
        } else {
          modOptions = { passive: true }
        }
      }
      return originalAddEventListener.call(this, type, listener, modOptions)
    }
  }
})
