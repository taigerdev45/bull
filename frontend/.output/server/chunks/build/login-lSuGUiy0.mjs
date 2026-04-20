import { ref, mergeProps, useSSRContext } from 'vue';
import { ssrRenderAttrs, ssrRenderAttr, ssrIncludeBooleanAttr } from 'vue/server-renderer';
import { useRouter } from 'vue-router';
import { u as useHead } from './composables-DdXMoNCu.mjs';
import { _ as _export_sfc } from './server.mjs';
import '../routes/renderer.mjs';
import 'vue-bundle-renderer/runtime';
import '../_/nitro.mjs';
import 'node:http';
import 'node:https';
import 'node:events';
import 'node:buffer';
import 'node:fs';
import 'node:path';
import 'node:crypto';
import 'node:url';
import 'unhead/server';
import 'devalue';
import 'unhead/utils';

const _sfc_main = {
  __name: "login",
  __ssrInlineRender: true,
  setup(__props) {
    useHead({
      title: "Connexion | LP ASUR"
    });
    useRouter();
    const username = ref("");
    const password = ref("");
    const loading = ref(false);
    return (_ctx, _push, _parent, _attrs) => {
      _push(`<div${ssrRenderAttrs(mergeProps({ class: "login-container" }, _attrs))} data-v-502fa904><div class="login-card" data-v-502fa904><div class="login-header" data-v-502fa904><h1 data-v-502fa904>Bull ASUR</h1><p data-v-502fa904>Connexion à l&#39;espace de gestion</p></div><form class="login-form" data-v-502fa904><div class="form-group" data-v-502fa904><label for="username" data-v-502fa904>Identifiant</label><input type="text" id="username"${ssrRenderAttr("value", username.value)} placeholder="Entrez votre identifiant" required data-v-502fa904></div><div class="form-group" data-v-502fa904><label for="password" data-v-502fa904>Mot de passe</label><input type="password" id="password"${ssrRenderAttr("value", password.value)} placeholder="Entrez votre mot de passe" required data-v-502fa904></div><button type="submit" class="login-btn"${ssrIncludeBooleanAttr(loading.value) ? " disabled" : ""} data-v-502fa904>`);
      if (!loading.value) {
        _push(`<span data-v-502fa904>Se Connecter</span>`);
      } else {
        _push(`<span class="loader" data-v-502fa904></span>`);
      }
      _push(`</button></form></div></div>`);
    };
  }
};
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("pages/login.vue");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const login = /* @__PURE__ */ _export_sfc(_sfc_main, [["__scopeId", "data-v-502fa904"]]);

export { login as default };
//# sourceMappingURL=login-lSuGUiy0.mjs.map
