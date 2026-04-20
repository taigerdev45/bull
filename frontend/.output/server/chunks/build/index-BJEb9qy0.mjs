import { ref, mergeProps, useSSRContext } from 'vue';
import { ssrRenderAttrs, ssrRenderList, ssrRenderClass, ssrInterpolate } from 'vue/server-renderer';
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
import 'vue-router';

const _sfc_main = {
  __name: "index",
  __ssrInlineRender: true,
  setup(__props) {
    useHead({
      title: "Délibérations | LP ASUR"
    });
    const resultats = ref([
      { id: "1001", nom: "Dupont", prenom: "Jean", moyS5: "12.45", ue1: "11.50", ue2: "13.20", credits: 30, decision: "Validé" },
      { id: "1002", nom: "Martin", prenom: "Sophie", moyS5: "14.80", ue1: "15.00", ue2: "14.65", credits: 30, decision: "Validé" },
      { id: "1003", nom: "Bernard", prenom: "Luc", moyS5: "9.20", ue1: "8.50", ue2: "9.80", credits: 0, decision: "Ajourné" },
      { id: "1004", nom: "Dubois", prenom: "Marie", moyS5: "10.15", ue1: "8.90", ue2: "11.20", credits: 30, decision: "Validé" }
    ]);
    return (_ctx, _push, _parent, _attrs) => {
      _push(`<div${ssrRenderAttrs(mergeProps({ class: "page-deliberation" }, _attrs))} data-v-1c93e9f2><header class="page-header" data-v-1c93e9f2><div class="header-content" data-v-1c93e9f2><h2 data-v-1c93e9f2>Délibérations du Jury (S5)</h2><p data-v-1c93e9f2>Année universitaire 2025-2026 - Liste récapitulative des résultats</p></div><div class="header-actions" data-v-1c93e9f2><button class="btn btn-secondary" data-v-1c93e9f2><span class="icon" data-v-1c93e9f2>📊</span> Exporter Excel </button><button class="btn btn-primary" data-v-1c93e9f2><span class="icon" data-v-1c93e9f2>✔️</span> Valider les décisions </button></div></header><div class="grid-container" data-v-1c93e9f2><table class="grid-delib" data-v-1c93e9f2><thead data-v-1c93e9f2><tr data-v-1c93e9f2><th data-v-1c93e9f2>Étudiant</th><th class="center" data-v-1c93e9f2>Moy S5</th><th class="center" data-v-1c93e9f2>UE5-1</th><th class="center" data-v-1c93e9f2>UE5-2</th><th class="center" data-v-1c93e9f2>Crédits</th><th class="center" data-v-1c93e9f2>Décision S5</th></tr></thead><tbody data-v-1c93e9f2><!--[-->`);
      ssrRenderList(resultats.value, (res) => {
        _push(`<tr class="${ssrRenderClass({ "is-failed": res.decision === "Ajourné" })}" data-v-1c93e9f2><td class="font-bold" data-v-1c93e9f2>${ssrInterpolate(res.nom)} ${ssrInterpolate(res.prenom)}</td><td class="center font-bold value" data-v-1c93e9f2>${ssrInterpolate(res.moyS5)}</td><td class="center" data-v-1c93e9f2>${ssrInterpolate(res.ue1)}</td><td class="center" data-v-1c93e9f2>${ssrInterpolate(res.ue2)}</td><td class="center badge-container" data-v-1c93e9f2><span class="${ssrRenderClass(["badge-sm", res.credits === 30 ? "badge-success" : "badge-warning"])}" data-v-1c93e9f2>${ssrInterpolate(res.credits)} / 30 </span></td><td class="center" data-v-1c93e9f2><span class="${ssrRenderClass(["decision-badge", res.decision === "Validé" ? "valid" : "invalid"])}" data-v-1c93e9f2>${ssrInterpolate(res.decision)}</span></td></tr>`);
      });
      _push(`<!--]--></tbody></table></div></div>`);
    };
  }
};
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("pages/deliberations/index.vue");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const index = /* @__PURE__ */ _export_sfc(_sfc_main, [["__scopeId", "data-v-1c93e9f2"]]);

export { index as default };
//# sourceMappingURL=index-BJEb9qy0.mjs.map
