import { mergeProps, useSSRContext } from 'vue';
import { ssrRenderAttrs } from 'vue/server-renderer';
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
      title: "Bulletins | LP ASUR"
    });
    return (_ctx, _push, _parent, _attrs) => {
      _push(`<div${ssrRenderAttrs(mergeProps({ class: "page-bulletins" }, _attrs))} data-v-68003675><header class="page-header" data-v-68003675><div class="header-content" data-v-68003675><h2 data-v-68003675>Bulletins Individuels</h2><p data-v-68003675>Générez et imprimez les bulletins (S5, S6, Annuel).</p></div><div class="header-actions" data-v-68003675><select class="type-select" data-v-68003675><option data-v-68003675>Semestre 5</option><option data-v-68003675>Semestre 6</option><option data-v-68003675>Annuel</option></select></div></header><div class="content-wrapper" data-v-68003675><div class="students-list" data-v-68003675><h3 data-v-68003675>Étudiants</h3><ul data-v-68003675><li class="active" data-v-68003675>Jean Dupont</li><li data-v-68003675>Sophie Martin</li><li data-v-68003675>Luc Bernard</li><li data-v-68003675>Marie Dubois</li></ul></div><div class="bulletin-preview" data-v-68003675><div class="pdf-toolbar" data-v-68003675><button class="btn btn-secondary" data-v-68003675><span class="icon" data-v-68003675>🔽</span> Télécharger PDF </button><button class="btn btn-primary" data-v-68003675><span class="icon" data-v-68003675>🖨️</span> Imprimer </button></div><div class="a4-sheet" data-v-68003675><div class="bulletin-header" data-v-68003675><div class="logo" data-v-68003675>INPTIC</div><div class="title-block" data-v-68003675><h1 data-v-68003675>BULLETIN DE NOTES - SEMESTRE 5</h1><h2 data-v-68003675>Licence Professionnelle ASUR</h2><p data-v-68003675>Année universitaire : 2025-2026</p></div><div class="student-info" data-v-68003675><p data-v-68003675><strong data-v-68003675>Nom:</strong> DUPONT</p><p data-v-68003675><strong data-v-68003675>Prénom:</strong> Jean</p><p data-v-68003675><strong data-v-68003675>ID:</strong> 1001</p></div></div><table class="bulletin-table" data-v-68003675><thead data-v-68003675><tr data-v-68003675><th data-v-68003675>Unité d&#39;Enseignement / Matière</th><th data-v-68003675>Coef.</th><th data-v-68003675>Note (/20)</th><th data-v-68003675>Moy. UE</th><th data-v-68003675>Crédits</th><th data-v-68003675>Absences</th></tr></thead><tbody data-v-68003675><tr class="ue-row" data-v-68003675><td colspan="3" data-v-68003675>UE5-1 : Enseignement Général</td><td class="center font-bold" data-v-68003675>11.50</td><td class="center font-bold" data-v-68003675>12</td><td data-v-68003675></td></tr><tr data-v-68003675><td class="indent" data-v-68003675>Anglais technique</td><td class="center" data-v-68003675>1</td><td class="center" data-v-68003675>14.00</td><td data-v-68003675></td><td class="center" data-v-68003675>2</td><td class="center" data-v-68003675>0h</td></tr><tr data-v-68003675><td class="indent" data-v-68003675>Communication</td><td class="center" data-v-68003675>2</td><td class="center" data-v-68003675>10.50</td><td data-v-68003675></td><td class="center" data-v-68003675>1</td><td class="center" data-v-68003675>0h</td></tr></tbody><tfoot data-v-68003675><tr data-v-68003675><th colspan="3" class="right" data-v-68003675>RÉSULTAT DU SEMESTRE</th><th class="center result-moy" data-v-68003675>12.45</th><th class="center result-cred" data-v-68003675>30</th><th data-v-68003675></th></tr></tfoot></table><div class="bulletin-footer" data-v-68003675><div class="decision-box" data-v-68003675><p data-v-68003675><strong data-v-68003675>Décision du Jury :</strong> Semestre 5 Validé</p></div><div class="signature" data-v-68003675><p data-v-68003675>Le Président du Jury,</p></div></div></div></div></div></div>`);
    };
  }
};
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("pages/bulletins/index.vue");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const index = /* @__PURE__ */ _export_sfc(_sfc_main, [["__scopeId", "data-v-68003675"]]);

export { index as default };
//# sourceMappingURL=index-D8gLDFzk.mjs.map
