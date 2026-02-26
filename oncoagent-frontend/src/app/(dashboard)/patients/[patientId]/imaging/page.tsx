"use client";

import { useParams } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

export default function ImagingPage() {
  const { patientId } = useParams<{ patientId: string }>();

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Imaging - Patient {patientId}</h1>
        <Badge variant="outline">DICOM Integration</Badge>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Card>
          <CardHeader>
            <CardTitle className="text-base">DICOM Viewer</CardTitle>
          </CardHeader>
          <CardContent className="h-64 flex items-center justify-center bg-muted/20 rounded">
            <p className="text-sm text-muted-foreground text-center">
              DICOM viewer placeholder.
              <br />
              Connect PACS/Orthanc via DICOMweb (WADO-RS, STOW-RS).
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-base">Tumor Metrics (RECIST 1.1)</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3 text-sm">
              <div className="flex justify-between">
                <span className="text-muted-foreground">Lesion Count</span>
                <span className="font-medium">--</span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Largest Diameter</span>
                <span className="font-medium">-- cm</span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">RECIST Response</span>
                <span className="font-medium">--</span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">AI Confidence</span>
                <span className="font-medium">--%</span>
              </div>
            </div>
            <p className="mt-3 text-xs text-muted-foreground">
              Powered by ImagingAgent. Data populates after scan analysis.
            </p>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Scan History</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground">
            No scans loaded. Connect PACS for imaging history with AI annotations.
          </p>
        </CardContent>
      </Card>
    </div>
  );
}
