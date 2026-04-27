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

      // Elegant Header
      doc.setFillColor(15, 23, 42) // Dark Navy
      doc.rect(0, 0, doc.internal.pageSize.width, 40, 'F')
      
      doc.setTextColor(255, 255, 255)
      doc.setFontSize(22)
      doc.setFont('helvetica', 'bold')
      doc.text('BULL ASUR', 15, 20)
      doc.setFontSize(10)
      doc.setFont('helvetica', 'normal')
      doc.text('Gestion Académique & Services Numériques', 15, 28)
      
      doc.setFontSize(8)
      doc.text(`Export : ${filename.toUpperCase()}`, doc.internal.pageSize.width - 15, 20, { align: 'right' })
      doc.text(`Date : ${new Date().toLocaleDateString()}`, doc.internal.pageSize.width - 15, 25, { align: 'right' })

      autoTable(doc, {
        head: [headers],
        body: rows,
        startY: 45,
        theme: 'striped',
        styles: { fontSize: 8, cellPadding: 4, font: 'helvetica' },
        headStyles: { fillColor: [15, 23, 42], textColor: 255, fontStyle: 'bold' },
        alternateRowStyles: { fillColor: [248, 250, 252] }
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

      // ─── 1. FILIGRANE DE SÉCURITÉ (Watermark) ───
      doc.setTextColor(245, 245, 245)
      doc.setFontSize(60)
      doc.setFont('helvetica', 'bold')
      doc.saveGraphicsState()
      doc.setGState(new doc.GState({ opacity: 0.1 }))
      doc.text('BULL ASUR OFFICIAL', pageWidth / 2, pageHeight / 2, { align: 'center', angle: 45 })
      doc.restoreGraphicsState()

      // ─── 2. EN-TETE INSTITUTIONNEL ───
      // Logo
      try {
        doc.addImage('/icon.png', 'PNG', 15, 12, 22, 22)
      } catch (e) {
        doc.setFillColor(15, 23, 42); doc.circle(26, 23, 10, 'F')
      }

      // QR Code
      const validationUrl = `https://bull-asur.ga/verify/${studentData.matricule || 'VALID'}`
      const qrApiUrl = `https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=${encodeURIComponent(validationUrl)}`
      try {
        doc.addImage(qrApiUrl, 'PNG', pageWidth - 42, 12, 28, 28)
      } catch (e) {}

      // Texte Central
      doc.setTextColor(15, 23, 42)
      doc.setFontSize(10)
      doc.setFont('times', 'bold')
      doc.text('RÉPUBLIQUE GABONAISE', pageWidth / 2, 15, { align: 'center' })
      doc.setFontSize(8)
      doc.setFont('times', 'italic')
      doc.text('Union - Travail - Justice', pageWidth / 2, 19, { align: 'center' })
      doc.setFont('helvetica', 'bold')
      doc.setFontSize(7)
      doc.text('INSTITUT NATIONAL DES POSTES ET TICS (INPTIC)', pageWidth / 2, 26, { align: 'center' })
      doc.setDrawColor(200); doc.setLineWidth(0.1); doc.line(75, 28, 135, 28)

      // ─── 3. TITRE DU BULLETIN ───
      doc.setTextColor(30, 45, 110)
      doc.setFontSize(18)
      doc.setFont('times', 'bold')
      doc.text(`BULLETIN DE NOTES DU SEMESTRE 5`, pageWidth / 2, 45, { align: 'center' })
      doc.setFontSize(11)
      doc.setFont('times', 'italic')
      doc.text(`Année Académique : 2025 - 2026`, pageWidth / 2, 51, { align: 'center' })

      // ─── 4. BANDEAU CLASSE ───
      doc.setFillColor(30, 45, 110)
      doc.rect(15, 58, pageWidth - 30, 10, 'F')
      doc.setTextColor(255, 255, 255)
      doc.setFontSize(9)
      doc.setFont('helvetica', 'bold')
      doc.text('Niveau : Licence Professionnelle Réseaux et Télécommunications (ASUR)', pageWidth / 2, 64.5, { align: 'center' })

      // ─── 5. INFOS ÉTUDIANT ───
      autoTable(doc, {
        startY: 72,
        margin: { left: 15 },
        tableWidth: pageWidth - 30,
        body: [
          ['NOM ET PRENOM(S)', studentData.nom + ' ' + studentData.prenom],
          ['MATRICULE', studentData.matricule || '2026-L3-0042'],
          ['DATE & LIEU DE NAISSANCE', '12 MAI 2004 À LIBREVILLE (GABON)']
        ],
        theme: 'grid',
        styles: { fontSize: 8.5, cellPadding: 2.5, textColor: [0, 0, 0], font: 'helvetica' },
        columnStyles: { 
          0: { cellWidth: 55, fontStyle: 'bold', fillColor: [245, 247, 250] }
        }
      })

      // ─── 6. TABLEAU DES NOTES (Ultra Refined) ───
      const gradeRows = [
        [{ content: 'UE5-1 : ENSEIGNEMENT GENERAL', colSpan: 5, styles: { fillColor: [235, 245, 255], fontStyle: 'bold', textColor: [20, 50, 120] } }],
        ['   Communication & Anglais', '4', '2.00', '15.50', '12.40'],
        ['   Management & Droit', '3', '1.50', '12.00', '11.10'],
        ['   Entreprenariat', '2', '1.00', '14.00', '13.00'],
        [{ content: 'MOYENNE UE5-1', colSpan: 3, styles: { halign: 'right', fontStyle: 'bold' } }, { content: '14.12', styles: { fontStyle: 'bold', fillColor: [250, 250, 250] } }, '12.16'],
        
        [{ content: 'UE5-2 : SYSTEMES ET RESEAUX', colSpan: 5, styles: { fillColor: [235, 245, 255], fontStyle: 'bold', textColor: [20, 50, 120] } }],
        ['   Réseaux Sans Fil (Wi-Fi/4G)', '5', '3.00', '11.50', '10.80'],
        ['   Sécurité Périmétrique', '4', '2.50', '13.00', '11.50'],
        ['   Services Réseaux Linux', '3', '2.00', '10.00', '11.20'],
        [{ content: 'MOYENNE UE5-2', colSpan: 3, styles: { halign: 'right', fontStyle: 'bold' } }, { content: '11.58', styles: { fontStyle: 'bold', fillColor: [250, 250, 250] } }, '11.16'],

        [{ content: 'TOTAL ET RESULTATS', colSpan: 5, styles: { fillColor: [245, 245, 245], fontStyle: 'bold' } }],
        [{ content: 'Bonus / Malus Absences', colSpan: 3, styles: { halign: 'right' } }, '0.00', ''],
        [{ content: 'MOYENNE GENERALE DU SEMESTRE', colSpan: 3, styles: { halign: 'right', fontStyle: 'bold', fontSize: 10 } }, { content: studentData.moyenne || '12.85', styles: { fontStyle: 'bold', fontSize: 10, fillColor: [30, 45, 110], textColor: 255 } }, '11.66']
      ]

      autoTable(doc, {
        startY: doc.lastAutoTable.finalY + 5,
        margin: { left: 15 },
        tableWidth: pageWidth - 30,
        head: [['INTITULÉ DES MATIÈRES / U.E', 'CRÉDITS', 'COEFF.', 'NOTE / 20', 'MOY. CLASSE']],
        body: gradeRows,
        theme: 'grid',
        styles: { fontSize: 8.5, cellPadding: 3, valign: 'middle' },
        headStyles: { fillColor: [30, 45, 110], textColor: 255, fontStyle: 'bold', halign: 'center' },
        columnStyles: {
          0: { cellWidth: 'auto' },
          1: { halign: 'center', cellWidth: 18 },
          2: { halign: 'center', cellWidth: 18 },
          3: { halign: 'center', cellWidth: 25 },
          4: { halign: 'center', cellWidth: 25 }
        }
      })

      // ─── 7. ETAT VALIDATION (Boxed Style) ───
      const validationY = doc.lastAutoTable.finalY + 8
      doc.setFillColor(250, 250, 250); doc.rect(15, validationY, pageWidth - 30, 20, 'F')
      doc.setDrawColor(200); doc.rect(15, validationY, pageWidth - 30, 20)
      
      doc.setTextColor(30, 45, 110); doc.setFontSize(9); doc.setFont('helvetica', 'bold')
      doc.text('BILAN DES CRÉDITS ECTS', pageWidth / 2, validationY + 6, { align: 'center' })
      
      doc.setTextColor(0); doc.setFontSize(8); doc.setFont('helvetica', 'normal')
      doc.text(`UE5-1 : 12 / 12 (Validé)`, 25, validationY + 13)
      doc.text(`UE5-2 : 18 / 18 (Validé)`, 85, validationY + 13)
      doc.text(`TOTAL : 30 / 30 (Admis)`, 145, validationY + 13)

      // ─── 8. DÉCISION DU JURY (Stamp Look) ───
      const juryY = validationY + 28
      doc.setDrawColor(30, 45, 110); doc.setLineWidth(0.5); doc.line(15, juryY, pageWidth - 15, juryY)
      
      doc.setFontSize(11); doc.setFont('times', 'bold')
      doc.text('DÉCISION DU JURY LEGISLATIF :', 20, juryY + 8)
      doc.setTextColor(15, 23, 42); doc.setFontSize(14)
      doc.text(studentData.decision || 'SEMESTRE VALIDÉ', 100, juryY + 9)
      doc.line(15, juryY + 16, pageWidth - 15, juryY + 16)

      // ─── 9. FOOTER & SIGNATURE ───
      const footerY = juryY + 30
      doc.setTextColor(0); doc.setFontSize(9); doc.setFont('times', 'bold')
      doc.text(`Délivré à Libreville, le ${new Date().toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' })}`, pageWidth - 20, footerY, { align: 'right' })
      doc.text('Le Directeur des Études et de la Pédagogie', pageWidth - 20, footerY + 8, { align: 'right' })
      
      // Decorative Seal
      doc.setDrawColor(30,45,110); doc.setLineWidth(0.2); doc.circle(pageWidth - 45, footerY + 25, 12)
      doc.setFontSize(5); doc.text('INPTIC - BULL ASUR\nSCEAU OFFICIEL', pageWidth - 45, footerY + 24, { align: 'center' })

      // Footer line
      doc.setFontSize(7); doc.setTextColor(150)
      doc.text('Ce document est une certification numérique. Vérifiez l\'original via le QR Code.', pageWidth / 2, pageHeight - 10, { align: 'center' })

      doc.save(`Bulletin_L3_ASUR_${studentData.nom}_S5.pdf`)
    } catch (e) {
      console.error(e)
      alert("Optimisation du style PDF échouée")
    }
  }

  return { exportToExcel, exportToPDF, generateBulletin }
}
