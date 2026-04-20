import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest, { params }: { params: { etudiantId: string } }) {
  return NextResponse.json({ message: 'Génération PDF pour ' + params.etudiantId });
}