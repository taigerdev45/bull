-- =================================================================
-- SCRIPT DE SECURITE SUPABASE (RLS & POLICIES)
-- Projet : Bulletin de Notes (LP ASUR)
-- Version : 1.1 (Correction permissions schéma auth)
-- =================================================================

-- 1. ACTIVATION DE LA RLS SUR TOUTES LES TABLES
ALTER TABLE public.django_models_semestremodel ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.django_models_uemodel ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.django_models_enseignantmodel ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.django_models_matieremodel ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.django_models_etudiantmodel ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.django_models_evaluationmodel ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.django_models_absencemodel ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.django_models_personnelmodel ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.django_models_auditlogmodel ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.django_models_parametreconfigmodel ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.django_models_resultatuemodel ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.django_models_resultatsemestremodel ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.django_models_resultatannuelmodel ENABLE ROW LEVEL SECURITY;

-- 2. FONCTION HELPER DANS LE SCHEMA PUBLIC (Plus sûr pour les permissions)
CREATE OR REPLACE FUNCTION public.get_role() 
RETURNS text AS $$
  SELECT (auth.jwt() -> 'user_metadata' ->> 'role')::text;
$$ LANGUAGE sql STABLE;

-- =================================================================
-- 3. POLITIQUES POUR LES ADMINISTRATEURS (Accès Total)
-- =================================================================
DO $$ 
DECLARE 
    t text;
BEGIN 
    FOR t IN SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_name LIKE 'django_models_%'
    LOOP
        EXECUTE format('DROP POLICY IF EXISTS "Admins have full access on %I" ON public.%I', t, t);
        EXECUTE format('CREATE POLICY "Admins have full access on %I" ON public.%I FOR ALL USING (public.get_role() = ''admin'')', t, t);
    END LOOP;
END $$;

-- =================================================================
-- 4. POLITIQUES POUR LE SECRETARIAT (Gestion globale sauf config critique)
-- =================================================================
DO $$ 
DECLARE 
    t text;
BEGIN 
    FOR t IN SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_name LIKE 'django_models_%' AND table_name != 'django_models_parametreconfigmodel'
    LOOP
        EXECUTE format('DROP POLICY IF EXISTS "Secretariat has full access on %I" ON public.%I', t, t);
        EXECUTE format('CREATE POLICY "Secretariat has full access on %I" ON public.%I FOR ALL USING (public.get_role() = ''secretariat'')', t, t);
    END LOOP;
END $$;

-- =================================================================
-- 5. POLITIQUES POUR LES ENSEIGNANTS
-- =================================================================

-- Lecture de tout pour le contexte académique
DO $$ 
DECLARE 
    t text;
BEGIN 
    FOR t IN SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_name LIKE 'django_models_%'
    LOOP
        EXECUTE format('DROP POLICY IF EXISTS "Enseignants can read %I" ON public.%I', t, t);
        EXECUTE format('CREATE POLICY "Enseignants can read %I" ON public.%I FOR SELECT USING (public.get_role() = ''enseignant'')', t, t);
    END LOOP;
END $$;

-- Écriture autorisée sur les évaluations et absences
DROP POLICY IF EXISTS "Enseignants can manage evaluations" ON public.django_models_evaluationmodel;
CREATE POLICY "Enseignants can manage evaluations" ON public.django_models_evaluationmodel 
    FOR ALL USING (public.get_role() = 'enseignant');

DROP POLICY IF EXISTS "Enseignants can manage absences" ON public.django_models_absencemodel;
CREATE POLICY "Enseignants can manage absences" ON public.django_models_absencemodel 
    FOR ALL USING (public.get_role() = 'enseignant');

-- =================================================================
-- 6. POLITIQUES POUR LES ETUDIANTS (Sécurité Stricte)
-- =================================================================

-- Lecture SEULE de leurs PROPRES données
DROP POLICY IF EXISTS "Etudiants can read their own info" ON public.django_models_etudiantmodel;
CREATE POLICY "Etudiants can read their own info" ON public.django_models_etudiantmodel 
    FOR SELECT USING (auth.uid()::text = user_id);

DROP POLICY IF EXISTS "Etudiants can read their own evaluations" ON public.django_models_evaluationmodel;
CREATE POLICY "Etudiants can read their own evaluations" ON public.django_models_evaluationmodel 
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM public.django_models_etudiantmodel e 
            WHERE e.id = etudiant_id AND e.user_id = auth.uid()::text
        )
    );

DROP POLICY IF EXISTS "Etudiants can read their own absences" ON public.django_models_absencemodel;
CREATE POLICY "Etudiants can read their own absences" ON public.django_models_absencemodel 
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM public.django_models_etudiantmodel e 
            WHERE e.id = etudiant_id AND e.user_id = auth.uid()::text
        )
    );

DROP POLICY IF EXISTS "Etudiants can read their own results" ON public.django_models_resultatannuelmodel;
CREATE POLICY "Etudiants can read their own results" ON public.django_models_resultatannuelmodel 
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM public.django_models_etudiantmodel e 
            WHERE e.id = etudiant_id AND e.user_id = auth.uid()::text
        )
    );

-- Idem pour les résultats UE et Semestre
DROP POLICY IF EXISTS "Etudiants can read their own UE results" ON public.django_models_resultatuemodel;
CREATE POLICY "Etudiants can read their own UE results" ON public.django_models_resultatuemodel 
    FOR SELECT USING (EXISTS (SELECT 1 FROM public.django_models_etudiantmodel e WHERE e.id = etudiant_id AND e.user_id = auth.uid()::text));

DROP POLICY IF EXISTS "Etudiants can read their own Semestre results" ON public.django_models_resultatsemestremodel;
CREATE POLICY "Etudiants can read their own Semestre results" ON public.django_models_resultatsemestremodel 
    FOR SELECT USING (EXISTS (SELECT 1 FROM public.django_models_etudiantmodel e WHERE e.id = etudiant_id AND e.user_id = auth.uid()::text));

-- Lecture globale autorisée pour les structures académiques (Matières, UE, Semestre)
DROP POLICY IF EXISTS "Etudiants can read structure" ON public.django_models_matieremodel;
CREATE POLICY "Etudiants can read structure" ON public.django_models_matieremodel FOR SELECT USING (public.get_role() = 'etudiant');

DROP POLICY IF EXISTS "Etudiants can read ues" ON public.django_models_uemodel;
CREATE POLICY "Etudiants can read ues" ON public.django_models_uemodel FOR SELECT USING (public.get_role() = 'etudiant');

DROP POLICY IF EXISTS "Etudiants can read semestres" ON public.django_models_semestremodel;
CREATE POLICY "Etudiants can read semestres" ON public.django_models_semestremodel FOR SELECT USING (public.get_role() = 'etudiant');
