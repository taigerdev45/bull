import { ref, resolveComponent, mergeProps, withCtx, createVNode, toDisplayString, useSSRContext } from 'vue';
import { ssrRenderAttrs, ssrRenderComponent, ssrRenderClass, ssrInterpolate } from 'vue/server-renderer';
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
      title: "Étudiants | LP ASUR"
    });
    const columns = [
      { key: "id", label: "ID", width: "80px" },
      { key: "nom", label: "Nom" },
      { key: "prenom", label: "Prénom" },
      { key: "bac", label: "Baccalauréat" },
      { key: "provenance", label: "Étab. Provenance" },
      { key: "status", label: "Statut", width: "120px" }
    ];
    const students = ref([
      { id: "1001", nom: "Dupont", prenom: "Jean", bac: "S", provenance: "Lycée A", status: "Inscrit" },
      { id: "1002", nom: "Martin", prenom: "Sophie", bac: "STI2D", provenance: "Lycée B", status: "Inscrit" },
      { id: "1003", nom: "Bernard", prenom: "Luc", bac: "Pro SN", provenance: "Lycée C", status: "Inscrit" },
      { id: "1004", nom: "Dubois", prenom: "Marie", bac: "S", provenance: "Lycée A", status: "Attente Jury" }
    ]);
    return (_ctx, _push, _parent, _attrs) => {
      const _component_DataTable = resolveComponent("DataTable");
      _push(`<div${ssrRenderAttrs(mergeProps({ class: "page-etudiants" }, _attrs))} data-v-ebd8f1ed><header class="page-header" data-v-ebd8f1ed><div class="header-content" data-v-ebd8f1ed><h2 data-v-ebd8f1ed>Gestion des Étudiants</h2><p data-v-ebd8f1ed>Gérez les élèves inscrits en Licence Professionnelle ASUR.</p></div><div class="header-actions" data-v-ebd8f1ed><button class="btn btn-secondary" data-v-ebd8f1ed><span class="icon" data-v-ebd8f1ed>📥</span> Importer (Excel) </button><button class="btn btn-primary" data-v-ebd8f1ed><span class="icon" data-v-ebd8f1ed>➕</span> Ajouter un Étudiant </button></div></header><div class="table-container" data-v-ebd8f1ed>`);
      _push(ssrRenderComponent(_component_DataTable, {
        title: "Liste de la Promotion",
        columns,
        data: students.value,
        actions: true
      }, {
        status: withCtx(({ row }, _push2, _parent2, _scopeId) => {
          if (_push2) {
            _push2(`<span class="${ssrRenderClass(["badge", row.status === "Inscrit" ? "badge-success" : "badge-warning"])}" data-v-ebd8f1ed${_scopeId}>${ssrInterpolate(row.status)}</span>`);
          } else {
            return [
              createVNode("span", {
                class: ["badge", row.status === "Inscrit" ? "badge-success" : "badge-warning"]
              }, toDisplayString(row.status), 3)
            ];
          }
        }),
        rowActions: withCtx(({ row }, _push2, _parent2, _scopeId) => {
          if (_push2) {
            _push2(`<button class="action-btn view-btn" title="Voir le profil" data-v-ebd8f1ed${_scopeId}>👁️</button><button class="action-btn edit-btn" title="Modifier" data-v-ebd8f1ed${_scopeId}>✏️</button><button class="action-btn delete-btn" title="Supprimer" data-v-ebd8f1ed${_scopeId}>🗑️</button>`);
          } else {
            return [
              createVNode("button", {
                class: "action-btn view-btn",
                title: "Voir le profil"
              }, "👁️"),
              createVNode("button", {
                class: "action-btn edit-btn",
                title: "Modifier"
              }, "✏️"),
              createVNode("button", {
                class: "action-btn delete-btn",
                title: "Supprimer"
              }, "🗑️")
            ];
          }
        }),
        _: 1
      }, _parent));
      _push(`</div></div>`);
    };
  }
};
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("pages/etudiants/index.vue");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const index = /* @__PURE__ */ _export_sfc(_sfc_main, [["__scopeId", "data-v-ebd8f1ed"]]);

export { index as default };
//# sourceMappingURL=index-DgLPmduN.mjs.map
