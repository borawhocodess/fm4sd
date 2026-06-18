.PHONY: main clean view FORCE

BUILD := build

main: $(BUILD)/thm31.pdf

# tectonic is the engine installed on this machine (not latexmk/lualatex).
# First run downloads a few packages/fonts, then caches them.
$(BUILD)/thm31.pdf: thm31.tex FORCE | $(BUILD)
	tectonic -X compile thm31.tex --outdir $(BUILD)

$(BUILD):
	mkdir -p $(BUILD)

view: main
	open $(BUILD)/thm31.pdf

clean:
	rm -rf $(BUILD)
