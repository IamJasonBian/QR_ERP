SET QUOTED_IDENTIFIER ON
GO
SET ANSI_NULLS ON
GO
CREATE PROCEDURE [dbo].[Increment_Component]
    (
    @Compid int 
    )
AS
BEGIN 
SET NOCOUNT ON

UPDATE Components
SET Quantity = Quantity + 1 
Where [Component ID] = @Compid

END

GO
