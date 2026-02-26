import { render, screen } from "@testing-library/react";
import { ConfidenceBadge } from "../ConfidenceBadge";

describe("ConfidenceBadge", () => {
  it("renders confidence percentage", () => {
    render(<ConfidenceBadge confidence={0.85} />);
    expect(screen.getByText(/85% confidence/)).toBeInTheDocument();
  });
});
