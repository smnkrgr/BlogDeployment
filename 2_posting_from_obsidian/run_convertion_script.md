<%*
// Execute the Python script and capture output
const { execSync } = require('child_process');

try {
    // Run the Python script, capture stdout and stderr
    const output = execSync('python3 "/home/user/Documents/BlogDeployment/2_posting_from_obsidian/convert_obsidian_to_jekyll.py"', { encoding: 'utf-8' });

    // Insert the output directly into the note
    tR += "```\n" + output + "\n```";
} catch (error) {
    // If script fails, show error in note
    tR += "❌ Error executing conversion script:\n```\n" + error.message + "\n```";
}
%>

