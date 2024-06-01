import {
  BedrockRuntimeClient,
  ConverseCommand,
} from "@aws-sdk/client-bedrock-runtime";

const client = new BedrockRuntimeClient({ region: "us-east-1" });

const userMessage = "Explain 'rubber duck debugging' in one line.";

const conversation = [
  {
    role: "user",
    content: [{ text: userMessage }],
  },
];

const systemPrompt = [{ text: "You must always respond in rhymes." }];

const parameters = {
  maxTokens: 100,
  temperature: 0.9,
  topP: 0.5,
};

//const modelId = "anthropic.claude-3-haiku-20240307-v1:0";
//const modelId = "amazon.titan-text-express-v1"; // NG This model doesn't support system messages.
//const modelId = "ai21.j2-mid-v1"; // NG: NG This model doesn't support system messages.
const modelId = "cohere.command-light-text-v14"; // NG: NG This model doesn't support system messages.


const command = new ConverseCommand({
  system: systemPrompt,
  inferenceConfig: parameters,
  messages: conversation,
  modelId,
});

const response = await client.send(command);

const responseText = response.output.message.content[0].text;

console.log(responseText);
