"use client";

import { useParams } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

export default function GenomicsPage() {
  const { patientId } = useParams<{ patientId: string }>();

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Genomics - Patient {patientId}</h1>
        <Badge variant="outline">VCF / FHIR Genomics</Badge>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Variant Table</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b text-left text-muted-foreground">
                  <th className="p-2">Gene</th>
                  <th className="p-2">Variant</th>
                  <th className="p-2">Classification</th>
                  <th className="p-2">Actionability</th>
                  <th className="p-2">Evidence</th>
                </tr>
              </thead>
              <tbody>
                <tr className="border-b">
                  <td className="p-2" colSpan={5}>
                    <span className="text-muted-foreground">
                      No genomic data loaded. Upload VCF or connect FHIR Genomics
                      (MolecularSequence, DiagnosticReport).
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <p className="mt-2 text-xs text-muted-foreground">
            Sources: ClinVar, COSMIC, OncoKB. Analyzed by genomic_variant_classifier.
          </p>
        </CardContent>
      </Card>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Pathway Viewer</CardTitle>
          </CardHeader>
          <CardContent className="h-48 flex items-center justify-center bg-muted/20 rounded">
            <p className="text-sm text-muted-foreground">
              Pathway visualization placeholder (D3.js).
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-base">Drug-Gene Interaction Matrix</CardTitle>
          </CardHeader>
          <CardContent className="h-48 flex items-center justify-center bg-muted/20 rounded">
            <p className="text-sm text-muted-foreground">
              Interaction matrix placeholder. Powered by drug_interaction_gnn.
            </p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
