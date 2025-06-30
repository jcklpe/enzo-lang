const vscode = require('vscode');

function activate(context) {
    // Apply custom token colors for Enzo language
    const config = vscode.workspace.getConfiguration();
    const existingRules = config.get('editor.tokenColorCustomizations.textMateRules') || [];

    const enzoRules = [
        {
            scope: "keyword.operator.enzo",
            settings: {
                foreground: "#FF8C00"
            }
        },
        {
            scope: "constant.numeric",
            settings: {
                foreground: "#FFD700"
            }
        }
    ];

    // Merge with existing rules if they don't already include our Enzo rules
    const hasEnzoRules = existingRules.some(rule =>
        rule.scope && (rule.scope.includes('enzo') || rule.scope.includes('keyword.operator.enzo'))
    );

    if (!hasEnzoRules) {
        const newRules = [...existingRules, ...enzoRules];
        config.update('editor.tokenColorCustomizations', {
            textMateRules: newRules
        }, vscode.ConfigurationTarget.Global);
    }
}

function deactivate() {}

module.exports = {
    activate,
    deactivate
};
