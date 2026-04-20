import { _ as __nuxt_component_0 } from './nuxt-link-D_XkvJJP.mjs';
import { computed, mergeProps, withCtx, createVNode, createTextVNode, useSSRContext } from 'vue';
import { ssrRenderAttrs, ssrRenderComponent, ssrInterpolate, ssrRenderSlot } from 'vue/server-renderer';
import { useRoute } from 'vue-router';
import { _ as _export_sfc } from './server.mjs';
import '../_/nitro.mjs';
import 'node:http';
import 'node:https';
import 'node:events';
import 'node:buffer';
import 'node:fs';
import 'node:path';
import 'node:crypto';
import 'node:url';
import '../routes/renderer.mjs';
import 'vue-bundle-renderer/runtime';
import 'unhead/server';
import 'devalue';
import 'unhead/utils';

const _sfc_main = {
  __name: "default",
  __ssrInlineRender: true,
  setup(__props) {
    const route = useRoute();
    const currentRoute = computed(() => {
      const path = route.path;
      if (path === "/") return "Dashboard";
      return path.substring(1).charAt(0).toUpperCase() + path.substring(2);
    });
    return (_ctx, _push, _parent, _attrs) => {
      const _component_NuxtLink = __nuxt_component_0;
      _push(`<div${ssrRenderAttrs(mergeProps({ class: "app-layout" }, _attrs))} data-v-8de7c164><aside class="sidebar" data-v-8de7c164><div class="sidebar-header" data-v-8de7c164><h1 data-v-8de7c164>Bull ASUR</h1></div><nav class="sidebar-nav" data-v-8de7c164>`);
      _push(ssrRenderComponent(_component_NuxtLink, {
        to: "/",
        class: "nav-link"
      }, {
        default: withCtx((_, _push2, _parent2, _scopeId) => {
          if (_push2) {
            _push2(`<span class="icon" data-v-8de7c164${_scopeId}>📊</span> Dashboard `);
          } else {
            return [
              createVNode("span", { class: "icon" }, "📊"),
              createTextVNode(" Dashboard ")
            ];
          }
        }),
        _: 1
      }, _parent));
      _push(ssrRenderComponent(_component_NuxtLink, {
        to: "/etudiants",
        class: "nav-link"
      }, {
        default: withCtx((_, _push2, _parent2, _scopeId) => {
          if (_push2) {
            _push2(`<span class="icon" data-v-8de7c164${_scopeId}>🎓</span> Étudiants `);
          } else {
            return [
              createVNode("span", { class: "icon" }, "🎓"),
              createTextVNode(" Étudiants ")
            ];
          }
        }),
        _: 1
      }, _parent));
      _push(ssrRenderComponent(_component_NuxtLink, {
        to: "/saisie",
        class: "nav-link"
      }, {
        default: withCtx((_, _push2, _parent2, _scopeId) => {
          if (_push2) {
            _push2(`<span class="icon" data-v-8de7c164${_scopeId}>📝</span> Saisie Notes `);
          } else {
            return [
              createVNode("span", { class: "icon" }, "📝"),
              createTextVNode(" Saisie Notes ")
            ];
          }
        }),
        _: 1
      }, _parent));
      _push(ssrRenderComponent(_component_NuxtLink, {
        to: "/referentiels",
        class: "nav-link"
      }, {
        default: withCtx((_, _push2, _parent2, _scopeId) => {
          if (_push2) {
            _push2(`<span class="icon" data-v-8de7c164${_scopeId}>📚</span> Référentiels `);
          } else {
            return [
              createVNode("span", { class: "icon" }, "📚"),
              createTextVNode(" Référentiels ")
            ];
          }
        }),
        _: 1
      }, _parent));
      _push(ssrRenderComponent(_component_NuxtLink, {
        to: "/deliberations",
        class: "nav-link"
      }, {
        default: withCtx((_, _push2, _parent2, _scopeId) => {
          if (_push2) {
            _push2(`<span class="icon" data-v-8de7c164${_scopeId}>⚖️</span> Délibérations `);
          } else {
            return [
              createVNode("span", { class: "icon" }, "⚖️"),
              createTextVNode(" Délibérations ")
            ];
          }
        }),
        _: 1
      }, _parent));
      _push(ssrRenderComponent(_component_NuxtLink, {
        to: "/bulletins",
        class: "nav-link"
      }, {
        default: withCtx((_, _push2, _parent2, _scopeId) => {
          if (_push2) {
            _push2(`<span class="icon" data-v-8de7c164${_scopeId}>📄</span> Bulletins `);
          } else {
            return [
              createVNode("span", { class: "icon" }, "📄"),
              createTextVNode(" Bulletins ")
            ];
          }
        }),
        _: 1
      }, _parent));
      _push(`</nav><div class="sidebar-footer" data-v-8de7c164>`);
      _push(ssrRenderComponent(_component_NuxtLink, {
        to: "/login",
        class: "nav-link logout-btn"
      }, {
        default: withCtx((_, _push2, _parent2, _scopeId) => {
          if (_push2) {
            _push2(`<span class="icon" data-v-8de7c164${_scopeId}>🚪</span> Déconnexion `);
          } else {
            return [
              createVNode("span", { class: "icon" }, "🚪"),
              createTextVNode(" Déconnexion ")
            ];
          }
        }),
        _: 1
      }, _parent));
      _push(`</div></aside><main class="main-content" data-v-8de7c164><header class="topbar" data-v-8de7c164><div class="breadcrumb" data-v-8de7c164><span data-v-8de7c164>${ssrInterpolate(currentRoute.value)}</span></div><div class="user-profile" data-v-8de7c164><div class="avatar" data-v-8de7c164>A</div><span data-v-8de7c164>Administrateur</span></div></header><div class="page-container" data-v-8de7c164>`);
      ssrRenderSlot(_ctx.$slots, "default", {}, null, _push, _parent);
      _push(`</div></main></div>`);
    };
  }
};
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("layouts/default.vue");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const _default = /* @__PURE__ */ _export_sfc(_sfc_main, [["__scopeId", "data-v-8de7c164"]]);

export { _default as default };
//# sourceMappingURL=default-gx1Zkr5i.mjs.map
