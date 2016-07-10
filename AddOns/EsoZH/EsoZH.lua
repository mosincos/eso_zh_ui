﻿local EsoZH = {}
EsoZH.name = "EsoZH"
EsoZH.Flags = { "en", "zh" }

function EsoZH_Change(lang)
	zo_callLater(function()
		SetCVar("language.2", lang)
		ReloadUI()
	end, 500)
end

function EsoZH:RefreshUI()
	local flagControl
	local count = 0
	local flagTexture
	for _, flagCode in pairs(EsoZH.Flags) do
		flagTexture = "EsoZH/flags/"..flagCode..".dds"
		flagControl = GetControl("EsoZH_FlagControl_"..tostring(flagCode))
		if flagControl == nil then
			flagControl = CreateControlFromVirtual("EsoZH_FlagControl_", EsoZHUI, "EsoZH_FlagControl", tostring(flagCode))
			GetControl("EsoZH_FlagControl_"..flagCode.."Texture"):SetTexture(flagTexture)
			if EsoZH:GetLanguage() ~= flagCode then
				flagControl:SetAlpha(0.3)
				if flagControl:GetHandler("OnMouseDown") == nil then flagControl:SetHandler("OnMouseDown", function() EsoZH_Change(flagCode) end) end
			end
		end
		flagControl:ClearAnchors()
		flagControl:SetAnchor(LEFT, EsoZHUI, LEFT, 14 +count*34, 0)
		count = count + 1
	end
	EsoZHUI:SetDimensions(25 +count*34, 50)
	EsoZHUI:SetMouseEnabled(true)
end

function EsoZH:GetLanguage()
	local lang = GetCVar("language.2")
	
	if(lang == "zh") then return lang end
	return "en"
end

function EsoZH:OnInit(eventCode, addOnName)
	if (addOnName):find("^ZO_") then return end

	for _, flagCode in pairs(EsoZH.Flags) do
		ZO_CreateStringId("SI_BINDING_NAME_"..string.upper(flagCode), string.upper(flagCode))
	end

	EsoZH:RefreshUI()
    
	function ZO_GameMenu_OnShow(control)
		if control.OnShow then
			control.OnShow(control.gameMenu)
			EsoZHUI:SetHidden(hidden)
		end
	end
	
	function ZO_GameMenu_OnHide(control)
		if control.OnHide then
			control.OnHide(control.gameMenu)
			EsoZHUI:SetHidden(not hidden)
		end
	end
end

EVENT_MANAGER:RegisterForEvent("EsoZH_OnAddOnLoaded", EVENT_ADD_ON_LOADED, function(_event, _name) EsoZH:OnInit(_event, _name) end)
