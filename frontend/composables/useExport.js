export const useExport = () => {
  const exportToExcel = async (data, filename = 'export.xlsx') => {
    if (!process.client) return
    if (!data || !data.length) return alert("Aucune donnée à exporter")
    
    try {
      const XLSX = await import('xlsx')
      const worksheet = XLSX.utils.json_to_sheet(data)
      const workbook = XLSX.utils.book_new()
      XLSX.utils.book_append_sheet(workbook, worksheet, 'Données')
      XLSX.writeFile(workbook, filename)
    } catch (error) {
      console.error("Erreur Excel:", error)
      alert("Erreur lors de la génération Excel.")
    }
  }

  const exportToPDF = async (headers, rows, filename = 'export.pdf', orientation = 'p') => {
    if (!process.client) return
    if (!rows || !rows.length) return alert("Aucune donnée à exporter")

    try {
      const { jsPDF } = await import('jspdf')
      const autoTable = (await import('jspdf-autotable')).default

      const doc = new jsPDF({
        orientation: orientation,
        unit: 'mm',
        format: 'a4'
      })

      // Header Monochrome
      doc.setFillColor(0, 0, 0)
      doc.rect(0, 0, doc.internal.pageSize.width, 35, 'F')
      
      doc.setTextColor(255, 255, 255)
      doc.setFontSize(20)
      doc.setFont('helvetica', 'bold')
      doc.text('BULL ASUR - GESTION ACADÉMIQUE', 15, 18)
      
      doc.setFontSize(9)
      doc.setFont('helvetica', 'normal')
      doc.text(`Document : ${filename.toUpperCase()}`, 15, 28)
      doc.text(`Date : ${new Date().toLocaleDateString()}`, doc.internal.pageSize.width - 60, 28)

      // Tableau Monochrome
      autoTable(doc, {
        head: [headers],
        body: rows,
        startY: 40,
        theme: 'grid',
        styles: { fontSize: 8, cellPadding: 3 },
        headStyles: { fillColor: [0, 0, 0], textColor: 255, fontStyle: 'bold' },
        alternateRowStyles: { fillColor: [245, 245, 245] }
      })

      doc.save(filename)
    } catch (error) {
      console.error("Erreur PDF:", error)
      alert("Erreur lors de la génération PDF.")
    }
  }

  const generateBulletin = async (studentData, type = 'semestriel') => {
    if (!process.client) return
    try {
      const { jsPDF } = await import('jspdf')
      const autoTable = (await import('jspdf-autotable')).default
      const doc = new jsPDF()
      
      const pageWidth = doc.internal.pageSize.width
      const pageHeight = doc.internal.pageSize.height

      // ─── STYLISATION PREMIUM ───
      // Bordure fine décorative
      doc.setDrawColor(230, 230, 230)
      doc.rect(5, 5, pageWidth - 10, pageHeight - 10)
      
      // Bande de sécurité latérale
      doc.setFillColor(0, 0, 0)
      doc.rect(0, 0, 3, pageHeight, 'F')

      // ─── LOGO (Simulation avec un cercle noir si absent, ou texte stylisé) ───
      // On tente d'ajouter l'icône du projet
      try {
        doc.addImage('/icon.png', 'PNG', 15, 10, 15, 15)
      } catch (e) {
        doc.setFillColor(0,0,0)
        doc.circle(22, 17, 8, 'F')
        doc.setTextColor(255,255,255)
        doc.setFontSize(10)
        doc.text('B', 20, 19)
      }

      // Header Officiel
      doc.setTextColor(0, 0, 0)
      doc.setFontSize(10)
      doc.setFont('helvetica', 'bold')
      doc.text('RÉPUBLIQUE GABONAISE', 105, 15, { align: 'center' })
      doc.setFontSize(8)
      doc.setFont('times', 'italic')
      doc.text('Union - Travail - Justice', 105, 20, { align: 'center' })
      
      doc.setFont('helvetica', 'normal')
      doc.setFontSize(7)
      doc.text('MINISTERE DE LA COMMUNICATION ET DE L\'ECONOMIE NUMERIQUE', 105, 28, { align: 'center' })
      doc.text('INSTITUT NATIONAL DES POSTES ET TICS (INPTIC)', 105, 32, { align: 'center' })
      
      // Titre du Document
      doc.setDrawColor(0,0,0)
      doc.setLineWidth(0.5)
      doc.line(70, 45, 140, 45)
      doc.setFontSize(16)
      doc.setFont('helvetica', 'bold')
      doc.text('BULLETIN DE NOTES', 105, 52, { align: 'center' })
      doc.setFontSize(11)
      doc.text(`${type.toUpperCase()} - SESSION 2025-2026`, 105, 60, { align: 'center' })
      doc.line(70, 65, 140, 65)

      // ─── INFOS ÉTUDIANT ───
      doc.setFillColor(245, 245, 245)
      doc.rect(15, 75, pageWidth - 30, 25, 'F')
      
      doc.setFontSize(10)
      doc.setTextColor(0,0,0)
      doc.setFont('helvetica', 'bold')
      doc.text(`Identité : ${studentData.nom} ${studentData.prenom}`, 20, 83)
      doc.setFont('helvetica', 'normal')
      doc.text(`Matricule : ${studentData.matricule || 'N/A'}`, 20, 90)
      doc.text(`Niveau : Licence 3 ASUR`, 20, 97)
      
      doc.text(`Date de naissance : 12/05/2004`, 120, 83)
      doc.text(`Lieu : Libreville`, 120, 90)
      doc.text(`Date d'édition : ${new Date().toLocaleDateString()}`, 120, 97)

      // ─── TABLEAU DES NOTES ───
      autoTable(doc, {
        startY: 110,
        head: [['Code UE', 'Unités d\'Enseignement / Matières', 'Note', 'Crédit', 'Résultat']],
        body: [
          [{ content: 'UE5.1', rowSpan: 2, styles: { valign: 'middle', fontStyle: 'bold' } }, 'Algorithmique & Structures de données', '14.50', '4', 'Validé'],
          ['Ingénierie Logicielle', '12.00', '3', 'Validé'],
          [{ content: 'UE5.2', rowSpan: 2, styles: { valign: 'middle', fontStyle: 'bold' } }, 'Réseaux Mobiles (4G/5G)', '16.00', '5', 'Validé'],
          ['Sécurité LAN/WAN', '11.50', '3', 'Validé'],
          [{ content: 'UE5.3', rowSpan: 2, styles: { valign: 'middle', fontStyle: 'bold' } }, 'Anglais Technique', '15.00', '2', 'Validé'],
          ['Droit de l\'informatique', '13.00', '2', 'Validé'],
        ],
        theme: 'grid',
        headStyles: { fillColor: [0, 0, 0], textColor: [255,255,255], fontStyle: 'bold' },
        styles: { fontSize: 9, cellPadding: 4 },
        columnStyles: { 
          0: { cellWidth: 25 },
          2: { halign: 'center', fontStyle: 'bold' },
          3: { halign: 'center' },
          4: { halign: 'center' }
        }
      })

      // ─── SYNTHÈSE & SIGNATURES ───
      const finalY = doc.lastAutoTable.finalY + 15
      
      doc.setFontSize(11)
      doc.setFont('helvetica', 'bold')
      doc.text(`MOYENNE GÉNÉRALE : ${studentData.moyenne || '0.00'} / 20`, 15, finalY)
      doc.setFontSize(10)
      doc.text(`DÉCISION DU JURY : ${studentData.decision || 'ADMISSIBLE'}`, 15, finalY + 7)
      
      // Ligne de signature
      doc.setFontSize(9)
      doc.text('Le Directeur des Études', pageWidth - 70, finalY)
      doc.setDrawColor(200, 200, 200)
      doc.line(pageWidth - 70, finalY + 2, pageWidth - 20, finalY + 2)
      
      // ─── QR CODE DE VÉRIFICATION ANTI-FRAUDE ───
      const validationUrl = `https://bull-asur.ga/verify/${studentData.matricule || 'VALID'}`
      const qrApiUrl = `https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=${encodeURIComponent(validationUrl)}`
      
      try {
        // Simple placeholder text if image fails, otherwise add QR
        doc.addImage(qrApiUrl, 'PNG', 15, pageHeight - 45, 30, 30)
        doc.setFontSize(6)
        doc.setTextColor(150, 150, 150)
        doc.text('Scanner pour vérifier l\'authenticité', 15, pageHeight - 12)
        doc.text(`ID: ${Math.random().toString(36).substr(2, 9).toUpperCase()}`, 15, pageHeight - 9)
      } catch (e) {
        doc.setFontSize(7)
        doc.text('[QR CODE DE SÉCURITÉ]', 15, pageHeight - 20)
      }

      // Mentions Légales
      doc.setFontSize(7)
      doc.setTextColor(100, 100, 100)
      doc.text('Certification Numérique Bull ASUR - Document officiel de l\'INPTIC', pageWidth / 2, pageHeight - 10, { align: 'center' })

      doc.save(`Bulletin_${studentData.nom}_${studentData.matricule}.pdf`)
    } catch (e) {
      console.error(e)
      alert("Échec de la génération stylisée du bulletin")
    }
  }

  return { exportToExcel, exportToPDF, generateBulletin }
}
