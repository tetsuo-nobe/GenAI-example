import {
  BedrockRuntimeClient,
  ConverseCommand,
} from "@aws-sdk/client-bedrock-runtime";

const client = new BedrockRuntimeClient({ region: "us-east-1" });

const firstMessage = "Explain 'rubber duck debugging' in one line.";

const firstResponse =
  "Rubber duck debugging is the process of explaining a problem to" +
  "an inanimate object, like a rubber duck, to help identify and" +
  "resolve the issue.";

const conversation = [
  { role: "user", content: [{ text: firstMessage }] },
  { role: "assistant", content: [{ text: firstResponse }] },
];

const newPrompt = "Okay. And does this actually work?";

const newMessage = { role: "user", content: [{ text: newPrompt }] };

conversation.push(newMessage);

//const modelId = "anthropic.claude-3-haiku-20240307-v1:0";
const modelId = "amazon.titan-text-express-v1";
//const modelId = "ai21.j2-mid-v1"; // NG: This model doesn't support conversation history.
//const modelId = "cohere.command-light-text-v14"; // NG: This model doesn't support conversation history.


const command = new ConverseCommand({
  modelId,
  messages: conversation,
});

const apiResponse = await client.send(command);

const responseText = apiResponse.output.message.content[0].text;
console.log(responseText);
