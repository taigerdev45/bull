// Imports client-side uniquement
import * as XLSX from 'xlsx'
import { jsPDF } from 'jspdf'
import 'jspdf-autotable'

export const useExport = () => {
  /**
   * Exporte des données vers un fichier Excel
   * @param {Array} data - Liste de dictionnaires d'objets
   * @param {String} filename - Nom du fichier de sortie
   */
  const exportToExcel = (data, filename = 'export.xlsx') => {
    if (!process.client) return
    if (!data || !data.length) return alert("Aucune donnée à exporter")
    
    try {
      const worksheet = XLSX.utils.json_to_sheet(data)
      const workbook = XLSX.utils.book_new()
      XLSX.utils.book_append_sheet(workbook, worksheet, 'Données')
      XLSX.writeFile(workbook, filename)
    } catch (error) {
      console.error("Erreur lors de l'export Excel:", error)
      alert("Erreur lors de la génération du fichier Excel.")
    }
  }

  /**
   * Exporte des données vers un fichier PDF
   * @param {Array} headers - Libellés des colonnes ['Nom', 'Prénom', ...]
   * @param {Array} rows - Valeurs correspondantes [['Doe', 'John'], ...]
   * @param {String} filename - Nom du fichier
   * @param {String} orientation - 'p' (portrait) ou 'l' (landscape)
   */
  const exportToPDF = (headers, rows, filename = 'export.pdf', orientation = 'p') => {
    if (!process.client) return
    if (!rows || !rows.length) return alert("Aucune donnée à exporter")

    const doc = new jsPDF({
      orientation: orientation,
      unit: 'mm',
      format: 'a4'
    })

    // Header stylisé
    doc.setFillColor(30, 41, 59) // bg-sidebar color
    doc.rect(0, 0, doc.internal.pageSize.width, 40, 'F')
    
    doc.setTextColor(255, 255, 255)
    doc.setFontSize(22)
    doc.text('BULL ASUR - GESTION ACADÉMIQUE', 14, 20)
    
    doc.setFontSize(10)
    doc.text(`Document : ${filename.replace('.pdf', '').toUpperCase()}`, 14, 30)
    doc.text(`Généré le : ${new Date().toLocaleString()}`, doc.internal.pageSize.width - 70, 30)

    // Tableau
    doc.autoTable({
      head: [headers],
      body: rows,
      startY: 45,
      theme: 'grid',
      styles: {
        fontSize: 9,
        cellPadding: 3,
        overflow: 'linebreak',
        halign: 'left'
      },
      headStyles: {
        fillColor: [37, 99, 235],
        textColor: 255,
        fontStyle: 'bold'
      },
      alternateRowStyles: {
        fillColor: [248, 250, 252]
      }
    })

    // Footer avec numérotation
    const pageCount = doc.internal.getNumberOfPages()
    for (let i = 1; i <= pageCount; i++) {
      doc.setPage(i)
      doc.setFontSize(8)
      doc.setTextColor(150, 150, 150)
      doc.text(
        `Page ${i} sur ${pageCount}`,
        doc.internal.pageSize.width / 2,
        doc.internal.pageSize.height - 10,
        { align: 'center' }
      )
    }

    doc.save(filename)
  }

  return { 
    exportToExcel, 
    exportToPDF 
  }
}
