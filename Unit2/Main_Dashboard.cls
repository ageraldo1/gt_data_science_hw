VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "Sheet1"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = True
Option Explicit

Const analysisDashboardSheetName = "Main"

Dim headerOperation1(1) As String
Dim headerOperation2(3) As String
Dim headerOperation3(6) As String


Private Sub endAnalysis(totalRecords As Long)

Dim currentRow As Long
    
    With Worksheets.Item(analysisDashboardSheetName)
        currentRow = .Cells(.Rows.Count, 1).End(xlUp).Row
        
        .Cells(currentRow, 4).Value = Now()
        .Cells(currentRow, 5).Value = totalRecords
        .Cells(currentRow, 6).Value = .Cells(currentRow, 4).Value - .Cells(currentRow, 3).Value
        .Cells(currentRow, 6).NumberFormat = "hh:mm:ss"
    End With
    
    Application.ScreenUpdating = True

End Sub



Private Sub startAnalysis(sheetName As String, analysisType As String)

Dim nextRow As Long

    Application.ScreenUpdating = False
    
    With Worksheets.Item(analysisDashboardSheetName)
        nextRow = .Cells(.Rows.Count, 1).End(xlUp).Row + 1
        
        .Cells(nextRow, 1).Value = sheetName
        .Cells(nextRow, 2).Value = analysisType
        .Cells(nextRow, 3).Value = Now()
    End With
    
End Sub

Private Function loadADT(analysisType As Integer, activeSheet As Worksheet) As Object
 
Dim tickerADT As Object

Dim lastRow As Long
Dim tickerName As String
Dim tickerVolume As Double
Dim tickerValues(6) As Variant
Dim i As Long

    Set tickerADT = CreateObject("Scripting.Dictionary")
    
    lastRow = activeSheet.Range("A1").End(xlDown).Row
    
    If analysisType = 1 Then
        For i = 2 To lastRow
            tickerName = activeSheet.Cells(i, 1).Value
            tickerVolume = activeSheet.Cells(i, 7).Value
            
            With tickerADT
                If .Exists(tickerName) Then
                    .Item(tickerName) = .Item(tickerName) + tickerVolume
                Else
                    .Add tickerName, tickerVolume
                End If
            End With
        Next
        
    ElseIf analysisType = 2 Then
        ' (0) = date_open
        ' (1) = date_close
        ' (2) = open
        ' (3) = close
        ' (4) = yearly change = closed - open
        ' (5) = % change = yearly change / open
        ' (6) = total stock volume
        
        For i = 2 To lastRow
            tickerName = activeSheet.Cells(i, 1).Value
            
            tickerValues(0) = activeSheet.Cells(i, 2).Value
            tickerValues(1) = activeSheet.Cells(i, 2).Value
            tickerValues(2) = activeSheet.Cells(i, 3).Value
            tickerValues(3) = activeSheet.Cells(i, 6).Value
            tickerValues(4) = tickerValues(3) - tickerValues(2)
            
            If (tickerValues(2) > 0) Then
                tickerValues(5) = tickerValues(4) / tickerValues(2)
            Else
                tickerValues(5) = 0
            End If
                
            tickerValues(6) = activeSheet.Cells(i, 7).Value
            
            With tickerADT
                If .Exists(tickerName) Then
                
                    If DateDiff("d", CDate(Mid(tickerValues(0), 1, 4) & "-" & Mid(tickerValues(0), 5, 2) & "-" & Mid(tickerValues(0), 7)), CDate(Mid(.Item(tickerName)(0), 1, 4) & "-" & Mid(.Item(tickerName)(0), 5, 2) & "-" & Mid(.Item(tickerName)(0), 7))) < 0 Then
                        tickerValues(0) = .Item(tickerName)(0)
                        tickerValues(2) = .Item(tickerName)(2)
                    End If
                    
                    If DateDiff("d", CDate(Mid(tickerValues(1), 1, 4) & "-" & Mid(tickerValues(1), 5, 2) & "-" & Mid(tickerValues(1), 7)), CDate(Mid(.Item(tickerName)(1), 1, 4) & "-" & Mid(.Item(tickerName)(1), 5, 2) & "-" & Mid(.Item(tickerName)(1), 7))) > 0 Then
                        tickerValues(1) = .Item(tickerName)(1)
                        tickerValues(3) = .Item(tickerName)(3)
                    End If
                    
                    tickerValues(4) = tickerValues(3) - tickerValues(2)
                    
                    If (tickerValues(2) > 0) Then
                        tickerValues(5) = tickerValues(4) / tickerValues(2)
                    Else
                        tickerValues(5) = 0
                    End If
                    
                    tickerValues(6) = .Item(tickerName)(6) + tickerValues(6)
                    
                    .Item(tickerName) = tickerValues
                Else
                    .Add tickerName, tickerValues
                End If
            End With
        Next
    End If
    
    Set loadADT = tickerADT

End Function

Private Sub cmd_clear_Click()

Dim activeSheet As Worksheet
Dim deleteRange As Range
Dim lastRow As Long
Dim lastColumn As Long
Dim i, y As Long

    For Each activeSheet In Worksheets
        If activeSheet.Name = analysisDashboardSheetName Then
            lastRow = activeSheet.Range("A3").End(xlDown).Row
            
            If lastRow <> activeSheet.Rows.Count Then
                For i = 4 To lastRow
                    With activeSheet
                        For y = 1 To 6
                            .Cells(i, y).Clear
                        Next
                    End With
                Next
            End If
        Else
            For i = 0 To UBound(headerOperation1)
                With activeSheet.UsedRange
                    Set deleteRange = .Find(What:=headerOperation1(i), MatchCase:=True, LookAt:=xlWhole)
                    
                    If Not deleteRange Is Nothing Then
                        deleteRange.EntireColumn.Delete
                    End If
                End With
            Next
            
            For i = 0 To UBound(headerOperation2)
                With activeSheet.UsedRange
                    Set deleteRange = .Find(What:=headerOperation2(i), MatchCase:=True, LookAt:=xlWhole)
                    
                    If Not deleteRange Is Nothing Then
                        deleteRange.EntireColumn.Delete
                    End If
                End With
            Next
            
            For i = 0 To UBound(headerOperation3)
                With activeSheet.UsedRange
                    Set deleteRange = .Find(What:=headerOperation3(i), MatchCase:=True, LookAt:=xlWhole)
                    
                    If Not deleteRange Is Nothing Then
                        deleteRange.EntireColumn.Delete
                    End If
                End With
            Next
        End If
    Next

End Sub

Private Sub cmd1_Click()

Dim tickerDict As Object
Dim tickerKey As Variant
Dim activeSheet As Worksheet
Dim nextColumn As Long

Dim i As Long

    Set tickerDict = CreateObject("Scripting.Dictionary")
    
    headerOperation1(0) = "Ticker"
    headerOperation1(1) = "Total Stock Volume"
    
    For Each activeSheet In Worksheets
        If activeSheet.Name <> analysisDashboardSheetName Then
            startAnalysis activeSheet.Name, cmd1.Caption
            
            '***** load data structure
            Set tickerDict = loadADT(1, activeSheet)
            
            '***** print data structure
            nextColumn = activeSheet.Range("A1").End(xlToRight).Column + 2
            
            i = 2
            With activeSheet
                .Cells(1, nextColumn).Value = headerOperation1(0)
                .Cells(1, nextColumn + 1).Value = headerOperation1(1)
                
                For Each tickerKey In tickerDict.Keys
                    .Cells(i, nextColumn).Value = tickerKey
                    .Cells(i, nextColumn + 1).Value = tickerDict.Item(tickerKey)
                    .Cells(i, nextColumn + 1).NumberFormat = "#,##0"
                    
                    i = i + 1
                Next
                
                .Cells.EntireColumn.AutoFit
                
            End With
            
            endAnalysis (tickerDict.Count)
        End If
    Next

End Sub

Private Sub cmd2_Click()

Dim tickerDict As Object
Dim tickerKey As Variant
Dim activeSheet As Worksheet
Dim nextColumn As Long
Dim i As Long

    Set tickerDict = CreateObject("Scripting.Dictionary")
    
    headerOperation2(0) = "Ticker"
    headerOperation2(1) = "Yearly Change"
    headerOperation2(2) = "Percent Change"
    headerOperation2(3) = "Total Stock Volume"
    
    For Each activeSheet In Worksheets
        If activeSheet.Name <> analysisDashboardSheetName Then
            startAnalysis activeSheet.Name, cmd2.Caption
            
            '***** load data structure
            Set tickerDict = loadADT(2, activeSheet)
            
            '***** print data structure
            nextColumn = activeSheet.Range("A1").End(xlToRight).Column + 2
            
            i = 2
            With activeSheet
                .Cells(1, nextColumn).Value = headerOperation2(0)
                .Cells(1, nextColumn + 1).Value = headerOperation2(1)
                .Cells(1, nextColumn + 2).Value = headerOperation2(2)
                .Cells(1, nextColumn + 3).Value = headerOperation2(3)
                
                For Each tickerKey In tickerDict.Keys
                    .Cells(i, nextColumn).Value = tickerKey
                    .Cells(i, nextColumn + 1).Value = tickerDict.Item(tickerKey)(4)
                    .Cells(i, nextColumn + 1).Interior.ColorIndex = IIf(tickerDict.Item(tickerKey)(4) > 0, 4, 3)
                    .Cells(i, nextColumn + 1).NumberFormat = "#,##0.000000000"
                    
                    .Cells(i, nextColumn + 2).Value = tickerDict.Item(tickerKey)(5)
                    .Cells(i, nextColumn + 2).NumberFormat = "0.00%"
                    
                    .Cells(i, nextColumn + 3).Value = tickerDict.Item(tickerKey)(6)
                    .Cells(i, nextColumn + 3).NumberFormat = "#,##0"
                    
                    i = i + 1
                Next
                
                .Cells.EntireColumn.AutoFit
            End With
            
            
            endAnalysis (tickerDict.Count)
        End If
    Next

End Sub


Private Sub cmd3_Click()

Dim tickerDict As Object
Dim tickerKey As Variant
Dim activeSheet As Worksheet
Dim nextColumn As Long
Dim i As Long

Dim gIncrease() As Variant
Dim gDecrease() As Variant
Dim gVolume() As Variant


    Set tickerDict = CreateObject("Scripting.Dictionary")
    
    headerOperation3(0) = "Ticker"
    headerOperation3(1) = "Yearly Change"
    headerOperation3(2) = "Percent Change"
    headerOperation3(3) = "Total Stock Volume"
    headerOperation3(4) = "Greatest Trends"
    headerOperation3(5) = "Ticker Trend"
    headerOperation3(6) = "Value"
    
    For Each activeSheet In Worksheets
        If activeSheet.Name <> analysisDashboardSheetName Then
        
            startAnalysis activeSheet.Name, cmd3.Caption
            
            '***** load data structure
            Set tickerDict = loadADT(2, activeSheet)
            
            '***** print data structure
            nextColumn = activeSheet.Range("A1").End(xlToRight).Column + 2
            
            i = 2
            With activeSheet
                .Cells(1, nextColumn).Value = headerOperation3(0)
                .Cells(1, nextColumn + 1).Value = headerOperation3(1)
                .Cells(1, nextColumn + 2).Value = headerOperation3(2)
                .Cells(1, nextColumn + 3).Value = headerOperation3(3)
                
                ReDim gIncrease(1), gDecrease(1), gVolume(1)
                
                For Each tickerKey In tickerDict.Keys
                    .Cells(i, nextColumn).Value = tickerKey
                    .Cells(i, nextColumn + 1).Value = tickerDict.Item(tickerKey)(4)
                    .Cells(i, nextColumn + 1).Interior.ColorIndex = IIf(tickerDict.Item(tickerKey)(4) > 0, 4, 3)
                    .Cells(i, nextColumn + 1).NumberFormat = "#,##0.000000000"
                    
                    .Cells(i, nextColumn + 2).Value = tickerDict.Item(tickerKey)(5)
                    .Cells(i, nextColumn + 2).NumberFormat = "0.00%"
                    
                    .Cells(i, nextColumn + 3).Value = tickerDict.Item(tickerKey)(6)
                    .Cells(i, nextColumn + 3).NumberFormat = "#,##0"
                    
                    
                    If (Len(gIncrease(0)) = 0 Or tickerDict.Item(tickerKey)(5) > gIncrease(1)) Then
                        gIncrease(0) = tickerKey
                        gIncrease(1) = tickerDict.Item(tickerKey)(5)
                    End If
                    
                    If (Len(gDecrease(0)) = 0 Or tickerDict.Item(tickerKey)(5) < gDecrease(1)) Then
                        gDecrease(0) = tickerKey
                        gDecrease(1) = tickerDict.Item(tickerKey)(5)
                    End If
                        
                    If (Len(gVolume(0)) = 0 Or tickerDict.Item(tickerKey)(6) > gVolume(1)) Then
                        gVolume(0) = tickerKey
                        gVolume(1) = tickerDict.Item(tickerKey)(6)
                    End If
                        
                    i = i + 1
                Next
                
                '*** greatest trends
                nextColumn = nextColumn + 5
                
                .Cells(1, nextColumn).Value = headerOperation3(4)
                .Cells(1, nextColumn + 1).Value = headerOperation3(5)
                .Cells(1, nextColumn + 2).Value = headerOperation3(6)
                
                .Cells(2, nextColumn).Value = "Greatest % Increase"
                .Cells(2, nextColumn + 1).Value = gIncrease(0)
                .Cells(2, nextColumn + 2).Value = gIncrease(1)
                .Cells(2, nextColumn + 2).NumberFormat = "0.00%"
                
                .Cells(3, nextColumn).Value = "Greatest % Decrease"
                .Cells(3, nextColumn + 1).Value = gDecrease(0)
                .Cells(3, nextColumn + 2).Value = gDecrease(1)
                .Cells(3, nextColumn + 2).NumberFormat = "0.00%"
                
                .Cells(4, nextColumn).Value = "Greatest Total Volume"
                .Cells(4, nextColumn + 1).Value = gVolume(0)
                .Cells(4, nextColumn + 2).Value = gVolume(1)
                .Cells(4, nextColumn + 2).NumberFormat = "#,##0"
                
                .Cells.EntireColumn.AutoFit
            End With
                        
            endAnalysis (tickerDict.Count)
        End If
    Next

End Sub
