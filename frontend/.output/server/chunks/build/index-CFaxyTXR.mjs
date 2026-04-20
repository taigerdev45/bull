import { ref, mergeProps, useSSRContext } from 'vue';
import { ssrRenderAttrs, ssrRenderList, ssrRenderClass, ssrInterpolate, ssrRenderAttr } from 'vue/server-renderer';
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
      title: "Saisie | LP ASUR"
    });
    const etudiants = ref([
      { id: "1001", nom: "Dupont", prenom: "Jean", cc: 14, exam: 10, ratrap: null, absences: 0 },
      { id: "1002", nom: "Martin", prenom: "Sophie", cc: 16, exam: 15, ratrap: null, absences: 2 },
      { id: "1003", nom: "Bernard", prenom: "Luc", cc: 8, exam: 6, ratrap: 11, absences: 4 },
      { id: "1004", nom: "Dubois", prenom: "Marie", cc: 12, exam: null, ratrap: null, absences: 0 }
    ]);
    const calculateMoyenne = (etudiant) => {
      if (etudiant.ratrap != null && etudiant.ratrap !== "") {
        return Number(etudiant.ratrap).toFixed(2);
      }
      if (etudiant.cc != null && etudiant.exam != null) {
        const moyenne = etudiant.cc * 0.4 + etudiant.exam * 0.6;
        return moyenne.toFixed(2);
      } else if (etudiant.cc != null) {
        return Number(etudiant.cc).toFixed(2);
      } else if (etudiant.exam != null) {
        return Number(etudiant.exam).toFixed(2);
      }
      return "-";
    };
    return (_ctx, _push, _parent, _attrs) => {
      _push(`<div${ssrRenderAttrs(mergeProps({ class: "page-saisie" }, _attrs))} data-v-96ba1d20><header class="page-header" data-v-96ba1d20><div class="header-content" data-v-96ba1d20><h2 data-v-96ba1d20>Saisie des Notes et Absences</h2><p data-v-96ba1d20>Semestre 5 - Anglais technique (UE5-1)</p></div><div class="header-actions" data-v-96ba1d20><select class="matiere-select" data-v-96ba1d20><option data-v-96ba1d20>S5 - Anglais technique</option><option data-v-96ba1d20>S5 - Management d&#39;équipe</option><option data-v-96ba1d20>S5 - Virtualisation</option></select><button class="btn btn-primary" data-v-96ba1d20><span class="icon" data-v-96ba1d20>💾</span> Enregistrer </button></div></header><div class="table-container" data-v-96ba1d20><table class="grid-saisie" data-v-96ba1d20><thead data-v-96ba1d20><tr data-v-96ba1d20><th width="80" data-v-96ba1d20>ID</th><th data-v-96ba1d20>Étudiant</th><th width="120" class="center" data-v-96ba1d20>Note CC (40%)</th><th width="120" class="center" data-v-96ba1d20>Examen (60%)</th><th width="120" class="center" data-v-96ba1d20>Rattrapage</th><th width="120" class="center" data-v-96ba1d20>Absences (h)</th><th width="120" class="center bg-gray" data-v-96ba1d20>Moyenne</th></tr></thead><tbody data-v-96ba1d20><!--[-->`);
      ssrRenderList(etudiants.value, (etudiant) => {
        _push(`<tr class="${ssrRenderClass({ "is-failed": calculateMoyenne(etudiant) < 10 && calculateMoyenne(etudiant) !== "-" })}" data-v-96ba1d20><td data-v-96ba1d20>${ssrInterpolate(etudiant.id)}</td><td class="font-bold" data-v-96ba1d20>${ssrInterpolate(etudiant.nom)} ${ssrInterpolate(etudiant.prenom)}</td><td class="center" data-v-96ba1d20><input type="number" min="0" max="20" step="0.25"${ssrRenderAttr("value", etudiant.cc)} class="grade-input" data-v-96ba1d20></td><td class="center" data-v-96ba1d20><input type="number" min="0" max="20" step="0.25"${ssrRenderAttr("value", etudiant.exam)} class="grade-input" data-v-96ba1d20></td><td class="center" data-v-96ba1d20><input type="number" min="0" max="20" step="0.25"${ssrRenderAttr("value", etudiant.ratrap)} class="grade-input" data-v-96ba1d20></td><td class="center" data-v-96ba1d20><input type="number" min="0"${ssrRenderAttr("value", etudiant.absences)} class="grade-input abscence" data-v-96ba1d20></td><td class="center bg-gray font-bold value-cell" data-v-96ba1d20>${ssrInterpolate(calculateMoyenne(etudiant))}</td></tr>`);
      });
      _push(`<!--]--></tbody></table></div></div>`);
    };
  }
};
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("pages/saisie/index.vue");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const index = /* @__PURE__ */ _export_sfc(_sfc_main, [["__scopeId", "data-v-96ba1d20"]]);

export { index as default };
//# sourceMappingURL=index-CFaxyTXR.mjs.map
