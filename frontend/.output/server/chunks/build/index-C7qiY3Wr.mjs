import { mergeProps, useSSRContext } from 'vue';
import { ssrRenderAttrs, ssrRenderStyle } from 'vue/server-renderer';
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
      title: "Dashboard | LP ASUR"
    });
    return (_ctx, _push, _parent, _attrs) => {
      _push(`<div${ssrRenderAttrs(mergeProps({ class: "dashboard" }, _attrs))} data-v-26c3a195><header class="dashboard-header" data-v-26c3a195><h2 data-v-26c3a195>Tableau de Bord - LP ASUR</h2><p class="subtitle" data-v-26c3a195>Vue d&#39;ensemble de l&#39;année pédagogique 2025-2026</p></header><div class="stats-grid" data-v-26c3a195><div class="stat-card" data-v-26c3a195><div class="stat-icon students" data-v-26c3a195>👥</div><div class="stat-content" data-v-26c3a195><h3 data-v-26c3a195>24</h3><p data-v-26c3a195>Étudiants Inscrits</p></div></div><div class="stat-card" data-v-26c3a195><div class="stat-icon modules" data-v-26c3a195>📚</div><div class="stat-content" data-v-26c3a195><h3 data-v-26c3a195>4</h3><p data-v-26c3a195>Unités d&#39;Enseignement (S5)</p></div></div><div class="stat-card" data-v-26c3a195><div class="stat-icon grades" data-v-26c3a195>✅</div><div class="stat-content" data-v-26c3a195><h3 data-v-26c3a195>65%</h3><p data-v-26c3a195>Notes Saisies</p></div></div><div class="stat-card" data-v-26c3a195><div class="stat-icon alert" data-v-26c3a195>⚠️</div><div class="stat-content" data-v-26c3a195><h3 data-v-26c3a195>2</h3><p data-v-26c3a195>Jury en Attente</p></div></div></div><div class="dashboard-widgets" data-v-26c3a195><div class="widget" data-v-26c3a195><h3 data-v-26c3a195>Dernières Activités</h3><ul class="activity-list" data-v-26c3a195><li data-v-26c3a195><span class="dot primary" data-v-26c3a195></span><strong data-v-26c3a195>M. Dupont</strong> a mis à jour les notes de <em data-v-26c3a195>Virtualisation</em>. <span class="time" data-v-26c3a195>Il y a 2h</span></li><li data-v-26c3a195><span class="dot success" data-v-26c3a195></span> Les bulletins du S5 ont été générés. <span class="time" data-v-26c3a195>Hier</span></li><li data-v-26c3a195><span class="dot warning" data-v-26c3a195></span> 15 absences enregistrées en <em data-v-26c3a195>Anglais Technique</em>. <span class="time" data-v-26c3a195>Il y a 3 jours</span></li></ul></div><div class="widget" data-v-26c3a195><h3 data-v-26c3a195>Répartition des Moyennes (S5)</h3><div class="chart-placeholder" data-v-26c3a195><div class="bar" style="${ssrRenderStyle({ "height": "30%" })}" data-v-26c3a195><span data-v-26c3a195>[0-10]</span></div><div class="bar" style="${ssrRenderStyle({ "height": "70%" })}" data-v-26c3a195><span data-v-26c3a195>[10-12]</span></div><div class="bar" style="${ssrRenderStyle({ "height": "100%" })}" data-v-26c3a195><span data-v-26c3a195>[12-14]</span></div><div class="bar" style="${ssrRenderStyle({ "height": "40%" })}" data-v-26c3a195><span data-v-26c3a195>[14-16]</span></div><div class="bar" style="${ssrRenderStyle({ "height": "10%" })}" data-v-26c3a195><span data-v-26c3a195>[16-20]</span></div></div></div></div></div>`);
    };
  }
};
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("pages/index.vue");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const index = /* @__PURE__ */ _export_sfc(_sfc_main, [["__scopeId", "data-v-26c3a195"]]);

export { index as default };
//# sourceMappingURL=index-C7qiY3Wr.mjs.map
