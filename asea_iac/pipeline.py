from aws_cdk import (
    core as cdk,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as cp_actions,
    aws_codecommit as codecommit,
    pipelines as pipelines
)

class EKSStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # REPO
        repo = codecommit.Repository(self, "IAC",
        repository_name="IAC",
        description="CDK IAC Pipeline."
        )

        # PIPELINE
        source_artifact = codepipeline.Artifact()
        
        pipeline = pipelines.CodePipeline(self, "Pipeline",
            synth=pipelines.ShellStep("Synth",
                input=pipelines.CodePipelineSource.code_commit(repo, "main"),
                commands=["pip install -r requirements.txt", "npm install -g aws-cdk", "cdk synth"]
            )
        )
        
        
        #pipeline = codepipeline.Pipeline(self, "EKSCTL",cross_account_keys=False)
        #source_stage = pipeline.add_stage(stage_name="Source", actions=[
        #    cp_actions.CodeCommitSourceAction(action_name='CodeCommit',repository=repo,output=source_artifact)
        #])
        